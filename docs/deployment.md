# Deployment

## Local Development

```bash
git clone https://github.com/amori27/data-engineering-portfolio.git
cd data-engineering-portfolio
make setup
```

## Production Considerations

### Kafka
- Increase replication factor to 3
- Use SSL encryption for inter-broker communication
- Configure retention based on data volume

### Spark
- Deploy on a cluster (EMR, Dataproc, or self-managed)
- Increase executors and memory for production throughput
- Enable checkpointing for fault tolerance

### API
- Deploy behind a reverse proxy (nginx, Caddy)
- Enable HTTPS via Let's Encrypt
- Use a process manager (supervisor, systemd)
- Scale horizontally behind a load balancer

### Database
- Use managed PostgreSQL (RDS, Cloud SQL)
- Enable automated backups
- Configure connection pooling (PgBouncer)
- Set up read replicas for heavy query loads

### Monitoring
- Kafka metrics via JMX Exporter + Prometheus
- Spark metrics via Spark Monitoring + Grafana
- API health checks for load balancer
- PostgreSQL slow query logging
