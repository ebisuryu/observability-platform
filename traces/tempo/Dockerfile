FROM grafana/tempo:2.6.1

USER root
RUN mkdir -p /var/tempo/wal /var/tempo/blocks && chown -R 10001:10001 /var/tempo
USER 10001

COPY tempo.yml /etc/tempo/tempo.yml

EXPOSE 3200 4317 4318

CMD ["-config.file=/etc/tempo/tempo.yml"]
