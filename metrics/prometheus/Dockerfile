FROM prom/prometheus:v2.53.0

COPY prometheus.yml /etc/prometheus/prometheus.yml
COPY rules /etc/prometheus/rules

EXPOSE 9090

CMD ["--config.file=/etc/prometheus/prometheus.yml", "--storage.tsdb.path=/prometheus", "--web.enable-lifecycle"]
