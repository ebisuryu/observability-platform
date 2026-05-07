import os
import random
import time

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import Status, StatusCode


SERVICE_NAME = os.getenv("SERVICE_NAME", "traces-demo")
ENVIRONMENT = os.getenv("ENVIRONMENT", "local")
SLEEP_SECONDS = float(os.getenv("SLEEP_SECONDS", "2"))
OTEL_EXPORTER_OTLP_ENDPOINT = os.getenv(
    "OTEL_EXPORTER_OTLP_ENDPOINT",
    "http://otel-collector:4317",
)


resource = Resource.create(
    {
        "service.name": SERVICE_NAME,
        "deployment.environment": ENVIRONMENT,
    }
)

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(
    OTLPSpanExporter(
        endpoint=OTEL_EXPORTER_OTLP_ENDPOINT,
        insecure=True,
    )
)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("traces-demo")


def sleep_ms(min_ms: int, max_ms: int) -> int:
    latency_ms = random.randint(min_ms, max_ms)
    time.sleep(latency_ms / 1000)
    return latency_ms


def emit_trace() -> None:
    request_id = f"req-{random.randint(1000, 9999)}"
    path = random.choice(["/health", "/api/orders", "/api/payments", "/api/users"])
    status_code = random.choices(
        population=[200, 201, 400, 404, 500],
        weights=[60, 10, 10, 10, 10],
        k=1,
    )[0]

    with tracer.start_as_current_span("http_request") as span:
        span.set_attribute("event", "http_request")
        span.set_attribute("request_id", request_id)
        span.set_attribute("http.method", "GET")
        span.set_attribute("http.route", path)
        span.set_attribute("http.status_code", status_code)
        span.set_attribute("service.name", SERVICE_NAME)
        span.set_attribute("deployment.environment", ENVIRONMENT)

        total_latency_ms = sleep_ms(20, 100)

        with tracer.start_as_current_span("validate_request") as child:
            child.set_attribute("request_id", request_id)
            sleep_ms(5, 30)

        if path != "/health":
            with tracer.start_as_current_span("database_query") as child:
                child.set_attribute("db.system", "postgresql")
                child.set_attribute("db.operation", "select")
                child.set_attribute("db.table", path.replace("/api/", ""))
                sleep_ms(20, 250)

        if path == "/api/payments":
            with tracer.start_as_current_span("payment_provider_call") as child:
                child.set_attribute("peer.service", "payment-provider-demo")
                child.set_attribute("http.method", "POST")
                sleep_ms(50, 500)

        if status_code >= 500:
            error = RuntimeError("request failed")
            span.record_exception(error)
            span.set_status(Status(StatusCode.ERROR, str(error)))
        elif status_code >= 400:
            span.set_status(Status(StatusCode.ERROR, "client error"))

        span.set_attribute("latency_ms", total_latency_ms)


if __name__ == "__main__":
    print(
        f"traces demo service started service={SERVICE_NAME} "
        f"environment={ENVIRONMENT} endpoint={OTEL_EXPORTER_OTLP_ENDPOINT}",
        flush=True,
    )

    while True:
        emit_trace()
        time.sleep(SLEEP_SECONDS)