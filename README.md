# Observability Platform

An opinionated local observability stack for collecting and exploring metrics, logs, and traces with Docker Compose.

This repository bundles a complete developer-friendly setup based on:

- `Prometheus` for metrics collection and alert rule evaluation
- `Loki` and `Promtail` for log aggregation
- `Tempo` for distributed tracing
- `OpenTelemetry Collector` for OTLP ingestion and telemetry routing
- `Grafana` for dashboards and exploration
- `Node Exporter` and `cAdvisor` for host and container metrics

It also includes small Python demo apps that generate logs, metrics, and traces so you can validate the stack end to end on a local machine.

## What this repo is for

Use this project when you want to:

- stand up a local observability environment quickly
- test telemetry pipelines before deploying to shared environments
- validate OpenTelemetry instrumentation
- inspect Docker host and container metrics
- explore logs and traces in Grafana with ready-to-use dashboards

## Architecture overview

The local flow is:

1. Demo apps emit logs, Prometheus metrics, or OTLP traces
2. `Promtail` scrapes Docker logs and pushes them to `Loki`
3. `Prometheus` scrapes exporters, Promtail, Loki, Grafana, and the metrics demo
4. `OpenTelemetry Collector` receives OTLP telemetry on ports `4317` and `4318`
5. The collector exports traces to `Tempo` and exposes OTLP-derived metrics for Prometheus scraping
6. `Grafana` is pre-provisioned with datasources and dashboards for exploration

## Repository structure

```text
.
├── README.md
├── collectors/
│   └── otel-collector/
├── dashboards/
│   └── grafana/
├── docs/
├── environments/
│   └── local/
├── examples/
│   ├── logs/
│   ├── metrics/
│   └── traces/
├── logs/
│   ├── loki/
│   └── promtail/
├── metrics/
│   ├── alertmanager/
│   ├── exporters/
│   └── prometheus/
└── traces/
    └── tempo/
```

Key directories:

- `environments/local`: the main Docker Compose stack for local development
- `collectors/otel-collector`: OpenTelemetry Collector image and pipeline config
- `metrics/prometheus`: Prometheus config and alert rules
- `logs/loki` and `logs/promtail`: log storage and collection
- `traces/tempo`: trace backend configuration
- `dashboards/grafana`: provisioned datasources and dashboards
- `examples/*`: demo services that generate sample telemetry
- `docs`: project documentation and operational notes

## Prerequisites

Before running the stack, make sure you have:

- Docker Engine or Docker Desktop
- Docker Compose v2
- enough local permissions for containers that mount host metrics and Docker logs

## Quick start

Start the full local observability stack:

```bash
docker compose -f environments/local/docker-compose.yml up -d --build
```

Open Grafana at `http://localhost:3000` and sign in with:

- Username: `admin`
- Password: `admin`

## Local endpoints

After the stack is running, these endpoints are available:

- Grafana: `http://localhost:3000`
- Prometheus: `http://localhost:9090`
- Loki: `http://localhost:3100`
- Tempo: `http://localhost:3200`
- OTel Collector gRPC: `http://localhost:4317`
- OTel Collector HTTP: `http://localhost:4318`
- OTel Collector health: `http://localhost:13133`
- Promtail metrics: `http://localhost:9080/metrics`

## Demo applications

This repository includes three small Python demo services:

- [examples/logs/README.md](/Users/long/Github/observability-platform/examples/logs/README.md): emits JSON logs to `stdout` for Loki ingestion
- [examples/metrics/README.md](/Users/long/Github/observability-platform/examples/metrics/README.md): exposes Prometheus metrics on port `8000`
- [examples/traces/README.md](/Users/long/Github/observability-platform/examples/traces/README.md): emits OTLP traces to the collector

Run them separately depending on what you want to validate.

### Logs demo

```bash
docker compose -f examples/logs/docker-compose.yml up --build
```

### Metrics demo

```bash
docker compose -f examples/metrics/docker-compose.yml up --build
```

### Traces demo

Make sure the local stack is already running first, then start:

```bash
docker compose -f examples/traces/docker-compose.yml up --build
```

The traces demo expects the external Docker network `local_observability`, which is created by the local stack Compose file.

## Viewing telemetry

### Logs

In Grafana:

1. Open `Explore`
2. Choose the `Loki` datasource
3. Run:

```logql
{compose_service="logs-demo"} | json
```

### Metrics

In Grafana or Prometheus, try:

```promql
up
```

For the metrics demo, query:

```promql
demo_requests_total
```

### Traces

In Grafana:

1. Open `Explore`
2. Choose the `Tempo` datasource
3. Open the `Search` tab
4. Filter by service `traces-demo`

You can also inspect collector logs directly:

```bash
docker logs -f observability-otel-collector
```

## Pre-provisioned dashboards

Grafana is preloaded with dashboards from [`dashboards/grafana/dashboards`](/Users/long/Github/observability-platform/dashboards/grafana/dashboards):

- `Metrics Overview`
- `Host Metrics`
- `Container Metrics`
- `Logs Overview`
- `Traces Overview`

## Configuration notes

The local stack uses a hybrid development model:

- images are built from local Dockerfiles for reproducibility
- configuration files are mounted directly for fast iteration

That means:

- editing a config file usually only requires restarting the relevant service
- changing a Dockerfile usually requires `--build`

Restart without rebuild:

```bash
docker compose -f environments/local/docker-compose.yml up -d
```

Rebuild when images change:

```bash
docker compose -f environments/local/docker-compose.yml up -d --build
```

## Important implementation details

- The OpenTelemetry Collector receives OTLP over both gRPC (`4317`) and HTTP (`4318`)
- The collector exports traces to `tempo:4317`
- Prometheus scrapes OTLP-derived metrics from the collector on `otel-collector:8889`
- The metrics demo is scraped through `host.docker.internal:8000`, so the demo should run on the host-published port as configured
- `Promtail` reads Docker container logs and host log paths directly from mounted volumes
- `Node Exporter` and `cAdvisor` require host-level mounts to expose system and container metrics

## Documentation

Additional docs are available in [`docs`](/Users/long/Github/observability-platform/docs):

- [docs/architecture.md](/Users/long/Github/observability-platform/docs/architecture.md)
- [docs/logging-guidelines.md](/Users/long/Github/observability-platform/docs/logging-guidelines.md)
- [`docs/runbooks`](/Users/long/Github/observability-platform/docs/runbooks)

## Useful entry points

- [environments/local/README.md](/Users/long/Github/observability-platform/environments/local/README.md)
- [metrics/exporters/README.md](/Users/long/Github/observability-platform/metrics/exporters/README.md)
- [collectors/otel-collector/config.yaml](/Users/long/Github/observability-platform/collectors/otel-collector/config.yaml)
- [metrics/prometheus/prometheus.yml](/Users/long/Github/observability-platform/metrics/prometheus/prometheus.yml)

## Known local-environment caveats

- On macOS or Windows with Docker Desktop, host-level dashboards reflect the Linux VM used by Docker, not the full native host OS
- The traces demo depends on the `local_observability` network created by the local stack
- Some components rely on privileged or host-mounted access, so behavior may vary slightly across operating systems

## Stopping the stack

Stop the local environment:

```bash
docker compose -f environments/local/docker-compose.yml down
```

Stop a demo app:

```bash
docker compose -f examples/logs/docker-compose.yml down
docker compose -f examples/metrics/docker-compose.yml down
docker compose -f examples/traces/docker-compose.yml down
```
