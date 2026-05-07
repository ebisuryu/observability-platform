observability-platform/
├── README.md
├── Makefile
│
├── environments/
│   └── local/
│       ├── docker-compose.yml
│       └── .env.example
│
├── collectors/
│   └── otel-collector/
│       ├── Dockerfile
│       └── config.yaml
│
├── exporters/
│   ├── README.md
│   ├── node-exporter/
│   │   └── Dockerfile
│   └── cadvisor/
│       └── Dockerfile
│
├── metrics/
│   ├── prometheus/
│   │   ├── Dockerfile
│   │   ├── prometheus.yml
│   │   └── rules/
│   │       └── service.rules.yml
│   │
│   └── alertmanager/
│       ├── Dockerfile
│       └── alertmanager.yml
│
├── logs/
│   ├── loki/
│   │   ├── Dockerfile
│   │   └── loki.yml
│   │
│   └── promtail/
│       ├── Dockerfile
│       └── promtail.yml
│
├── traces/
│   └── tempo/
│       ├── Dockerfile
│       └── tempo.yml
│
├── dashboards/
│   └── grafana/
│       ├── Dockerfile
│       ├── datasources/
│       │   ├── prometheus.yaml
│       │   ├── loki.yaml
│       │   ├── tempo.yaml
│       │   └── alertmanager.yaml
│       │
│       ├── dashboards/
│       │   ├── container-metrics.json
│       │   ├── host-metrics.json
│       │   ├── logs-overview.json
│       │   └── metrics-overview.json
│       │
│       └── provisioning/
│           ├── dashboards.yaml
│           └── datasources.yaml
│
├── deployment/
│   └── docker-compose/
│       └── docker-compose.observability.yml
│
├── scripts/
│   ├── bootstrap-local.sh
│   ├── validate-config.sh
│   └── check-health.sh
│
└── docs/
    ├── architecture.md
    ├── logging-guidelines.md
    └── runbooks/
        ├── log-ingestion-delay.md
        ├── high-error-rate.md
        └── service-down.md
