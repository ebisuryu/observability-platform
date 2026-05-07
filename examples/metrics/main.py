import os
import random
import time

from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import Histogram
from prometheus_client import start_http_server


SERVICE_NAME = os.getenv("SERVICE_NAME", "metrics-demo")
PORT = int(os.getenv("METRICS_PORT", "8000"))
SLEEP_SECONDS = float(os.getenv("SLEEP_SECONDS", "2"))

REQUEST_COUNTER = Counter(
    "demo_requests_total",
    "Total number of demo requests",
    ["service", "endpoint", "status_code"],
)

IN_PROGRESS_GAUGE = Gauge(
    "demo_requests_in_progress",
    "Number of in-progress demo requests",
    ["service"],
)

LATENCY_HISTOGRAM = Histogram(
    "demo_request_duration_seconds",
    "Latency of demo requests",
    ["service", "endpoint"],
    buckets=(0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0),
)


def simulate_request() -> None:
    endpoint = random.choice(
        ["/api/orders", "/api/payments", "/api/users", "/health"]
    )
    status_code = random.choices(
        population=["200", "201", "400", "404", "500"],
        weights=[60, 10, 10, 10, 10],
        k=1,
    )[0]
    duration = random.uniform(0.03, 1.8)

    IN_PROGRESS_GAUGE.labels(service=SERVICE_NAME).inc()
    try:
        time.sleep(duration)
        REQUEST_COUNTER.labels(
            service=SERVICE_NAME,
            endpoint=endpoint,
            status_code=status_code,
        ).inc()
        LATENCY_HISTOGRAM.labels(
            service=SERVICE_NAME,
            endpoint=endpoint,
        ).observe(duration)
    finally:
        IN_PROGRESS_GAUGE.labels(service=SERVICE_NAME).dec()


if __name__ == "__main__":
    start_http_server(PORT)
    while True:
        simulate_request()
        time.sleep(SLEEP_SECONDS)
