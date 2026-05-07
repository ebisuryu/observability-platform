# Logs Demo

This Python demo service emits JSON logs to `stdout` so that `promtail` can collect them from Docker container logs and push them to Loki.

## Files

- `Dockerfile`: builds the demo app image
- `main.py`: loop that generates simulated request logs
- `requirements.txt`: app dependencies

## Run standalone

```bash
docker build -t observability-logs-demo examples/logs
docker run --rm observability-logs-demo
```

## Run with its own Docker Compose file

From the `examples/logs` directory:

```bash
docker compose up --build
```

Or from the repository root:

```bash
docker compose -f examples/logs/docker-compose.yml up --build
```

## Run together with the local log stack

From the repository root:

```bash
docker compose -f environments/local/docker-compose.yml up --build
docker compose -f examples/logs/docker-compose.yml up --build
```

After startup:

- Loki: `http://localhost:3100`
- Promtail metrics: `http://localhost:9080/metrics`
- Collector health: `http://localhost:13133`

You can inspect the demo container logs with:

```bash
docker logs -f observability-logs-demo
```
