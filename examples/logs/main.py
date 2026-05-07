import json
import logging
import os
import random
import sys
import time
from datetime import datetime, timezone


LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
SERVICE_NAME = os.getenv("SERVICE_NAME", "logs-demo")
ENVIRONMENT = os.getenv("ENVIRONMENT", "local")
SLEEP_SECONDS = float(os.getenv("SLEEP_SECONDS", "2"))


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "service": SERVICE_NAME,
            "environment": ENVIRONMENT,
        }
        if hasattr(record, "event"):
            payload["event"] = record.event
        if hasattr(record, "request_id"):
            payload["request_id"] = record.request_id
        if hasattr(record, "path"):
            payload["path"] = record.path
        if hasattr(record, "status_code"):
            payload["status_code"] = record.status_code
        if hasattr(record, "latency_ms"):
            payload["latency_ms"] = record.latency_ms
        return json.dumps(payload)


handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JsonFormatter())

logger = logging.getLogger("logs-demo")
logger.setLevel(LOG_LEVEL)
logger.handlers.clear()
logger.addHandler(handler)
logger.propagate = False


def emit_log() -> None:
    request_id = f"req-{random.randint(1000, 9999)}"
    path = random.choice(["/health", "/api/orders", "/api/payments", "/api/users"])
    latency_ms = random.randint(20, 1500)
    status_code = random.choices(
        population=[200, 201, 400, 404, 500],
        weights=[60, 10, 10, 10, 10],
        k=1,
    )[0]

    if status_code >= 500:
        logger.error(
            "request failed",
            extra={
                "event": "http_request",
                "request_id": request_id,
                "path": path,
                "status_code": status_code,
                "latency_ms": latency_ms,
            },
        )
        return

    if status_code >= 400:
        logger.warning(
            "request completed with client error",
            extra={
                "event": "http_request",
                "request_id": request_id,
                "path": path,
                "status_code": status_code,
                "latency_ms": latency_ms,
            },
        )
        return

    logger.info(
        "request completed",
        extra={
            "event": "http_request",
            "request_id": request_id,
            "path": path,
            "status_code": status_code,
            "latency_ms": latency_ms,
        },
    )


if __name__ == "__main__":
    logger.info(
        "logs demo service started",
        extra={"event": "startup"},
    )
    while True:
        emit_log()
        time.sleep(SLEEP_SECONDS)
