FROM grafana/loki:3.0.0

COPY loki.yml /etc/loki/local-config.yaml

EXPOSE 3100

CMD ["-config.file=/etc/loki/local-config.yaml"]
