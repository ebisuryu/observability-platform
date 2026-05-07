# Traces Demo

This example is a very small Python app that uses OpenTelemetry to generate traces periodically and send them to the OpenTelemetry Collector over OTLP gRPC.

The app simulates requests such as:

- `/health`
- `/api/orders`
- `/api/payments`
- `/api/users`

Each trace has a parent span named `http_request` and may include child spans such as:

- `validate_request`
- `database_query`
- `payment_provider_call`

The sample also attaches useful attributes such as `request_id`, `http.route`, `http.status_code`, `service.name`, and `deployment.environment`.

## Purpose

Use this sample to:

- verify that the app can export traces to the collector
- observe the parent/child span structure
- simulate successful requests, client errors, and server errors
- test the trace pipeline in a local environment

## How it works

The app runs an infinite loop:

1. Generates a random simulated request
2. Creates a trace with one parent span
3. Adds child spans depending on the route
4. Marks error status when the HTTP status is `4xx` or `5xx`
5. Waits for `SLEEP_SECONDS` and repeats

## Run with the local stack

First start the observability stack:

```bash
docker compose -f environments/local/docker-compose.yml up -d --build
```

Then start the demo app:

```bash
docker compose -f examples/traces/docker-compose.yml up -d --build
```

The demo compose file attaches the container to the `local_observability` network so it can send traces to `otel-collector:4317`.

If you want to run it manually without Compose:

```bash
docker build -t observability/traces-demo:local examples/traces
docker run --rm \
  --name traces-demo \
  --network local_observability \
  -e SERVICE_NAME=traces-demo \
  -e ENVIRONMENT=local \
  -e OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317 \
  observability/traces-demo:local
```

If the Docker network on your machine has a different name, check it with:

```bash
docker network ls
```

When started from `environments/local/docker-compose.yml`, the network is typically `local_observability`.

## Run directly with Python

If you want to run it without Docker:

```bash
cd examples/traces
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317 python3 main.py
```

Notes:

- use `http://localhost:4317` when the app runs on the host
- use `http://otel-collector:4317` when the app runs in the same Docker network as the collector

## Environment variables

- `SERVICE_NAME`: service name, defaults to `traces-demo`
- `ENVIRONMENT`: deployment environment, defaults to `local`
- `SLEEP_SECONDS`: delay between trace emissions, defaults to `2`
- `OTEL_EXPORTER_OTLP_ENDPOINT`: OTLP gRPC endpoint, defaults to `http://otel-collector:4317`

## How to verify traces reached the collector

In the current configuration, `otel-collector` uses the `debug` exporter for the traces pipeline. That means you can inspect the collector logs to confirm that traces are being received:

```bash
docker logs -f observability-otel-collector
```

When the sample is working correctly, you should see spans printed by the collector with names such as:

- `http_request`
- `validate_request`
- `database_query`
- `payment_provider_call`

## Current note

The file [collectors/otel-collector/config.yaml](/Users/long/Github/observability-platform/collectors/otel-collector/config.yaml:1) is configured to export traces to `tempo:4317`, but `environments/local/docker-compose.yml` currently does not include a `tempo` service.

That means:

- the most reliable way to verify traces right now is to inspect the `otel-collector` logs
- if you want to view traces in a UI such as Grafana Tempo, you need to add the Tempo service and matching datasource to the local stack

## Related files

- [main.py](/Users/long/Github/observability-platform/examples/traces/main.py:1)
- [Dockerfile](/Users/long/Github/observability-platform/examples/traces/Dockerfile:1)
- [requirements.txt](/Users/long/Github/observability-platform/examples/traces/requirements.txt:1)
- [local stack README](/Users/long/Github/observability-platform/environments/local/README.md:1)
