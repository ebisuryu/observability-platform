FROM grafana/grafana:11.0.0

COPY provisioning /etc/grafana/provisioning
COPY datasources /etc/grafana/provisioning/datasources
COPY dashboards /var/lib/grafana/dashboards

EXPOSE 3000
