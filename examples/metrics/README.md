# Metrics Demo

This Python demo service exposes Prometheus metrics on port `8000` so Prometheus can scrape them and Grafana can visualize them.

## Files

- `Dockerfile`: builds the demo app image
- `main.py`: generates simulated requests and publishes metrics
- `requirements.txt`: app dependencies
- `docker-compose.yml`: runs the demo service on its own

## Run standalone

From the `examples/metrics` directory:

```bash
docker compose up --build
```

Or from the repository root:

```bash
docker compose -f examples/metrics/docker-compose.yml up --build
```

Metrics endpoint:

```text
http://localhost:8000
```

## Run together with the local metrics stack

From the repository root:

```bash
docker compose -f environments/local/docker-compose.yml up
docker compose -f examples/metrics/docker-compose.yml up --build
```

After startup:

- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`
- Demo metrics endpoint: `http://localhost:8000`

In Grafana, you can query:

```promql
demo_requests_total
```
