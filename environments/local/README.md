# Local Observability Stack

The local stack currently includes:

- Loki
- Promtail
- OpenTelemetry Collector
- Tempo
- Prometheus
- Grafana
- Node Exporter
- cAdvisor

## Run

From the repository root:

```bash
docker compose -f environments/local/docker-compose.yml up --build
```

If you also want the demo app that generates logs:

```bash
docker compose -f examples/logs/docker-compose.yml up --build
```

If you also want the demo app that generates metrics:

```bash
docker compose -f examples/metrics/docker-compose.yml up --build
```

If you also want the demo app that generates traces:

```bash
docker compose -f examples/traces/docker-compose.yml up --build
```

The local stack uses a hybrid approach:

- `build` keeps the image structure consistent
- `mount` is used for config and dashboard files that are frequently updated during local development

The following files are mounted directly:

- `logs/loki/loki.yml`
- `logs/promtail/promtail.yml`
- `collectors/otel-collector/config.yaml`
- `traces/tempo/tempo.yml`
- `dashboards/grafana/dashboards/*.json`
- `dashboards/grafana/datasources/*.yaml`
- `metrics/prometheus/prometheus.yml`
- `metrics/prometheus/rules/*.yml`

When you edit the files above, you usually only need to restart the service or rerun Compose, without rebuilding the images.

Example:

```bash
docker compose -f environments/local/docker-compose.yml up -d
```

You only need `--build` when you change a Dockerfile or want to rebuild the base images:

```bash
docker compose -f environments/local/docker-compose.yml up -d --build
```

## Endpoints

- Grafana: `http://localhost:3000`
- Loki: `http://localhost:3100`
- Tempo: `http://localhost:3200`
- Prometheus: `http://localhost:9090`
- Promtail metrics: `http://localhost:9080/metrics`
- OTel Collector health: `http://localhost:13133`

## Grafana login

- Username: `admin`
- Password: `admin`

## View logs

After running `examples/logs`, open Grafana and:

1. Open the `Logs Overview` dashboard
2. Or go to `Explore`
3. Select the `Loki` datasource
4. Run the query:

```logql
{compose_service="logs-demo"} | json
```

## View metrics

In Grafana:

1. Open `Metrics Overview`, `Host Metrics`, `Container Metrics`, or `Logs Overview`
2. Or go to `Explore`
3. Select the `Prometheus` datasource
4. Run a sample query:

```promql
up
```

## View traces

After running `examples/traces`, open Grafana and:

1. Open the `Traces Overview` dashboard
2. Or go to `Explore`
3. Select the `Tempo` datasource
4. Open the `Search` tab
5. Filter by the `traces-demo` service

You can also inspect the collector logs to confirm that traces are being received:

```bash
docker logs -f observability-otel-collector
```

## Metrics dashboards

The current dashboards include:

- `Metrics Overview`: target overview, demo metrics, and host/container summary
- `Host Metrics`: CPU, RAM, `/` disk, network, and disk I/O for the host
- `Container Metrics`: CPU, memory, restarts, network, and disk I/O per container
- `Logs Overview`: log volume and log streams from Loki
- `Traces Overview`: trace search for the `traces-demo` service from `examples/traces`

If you are starting the stack for the first time, run:

```bash
docker compose -f environments/local/docker-compose.yml up -d --build
```

If you only changed config or dashboards, you usually just need:

```bash
docker compose -f environments/local/docker-compose.yml up -d
```

Note: if you run Docker Desktop on macOS or Windows, the `Host` section in the dashboards reflects the Linux VM running the Docker engine. If you run Docker directly on a Linux host, those metrics belong to that host machine.
