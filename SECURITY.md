# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x     | ✅        |

## Reporting a Vulnerability

If you discover a security vulnerability, please do NOT open a public issue. Instead, email the details to amirasaadprog@gmail.com.

We will acknowledge receipt within 48 hours and work on a fix.

## Best Practices

- Never commit `.env` files or API keys to version control
- Use environment variables or a secrets manager for credentials
- Run Kafka and PostgreSQL in isolated Docker networks
- Rotate credentials regularly
- Enable encryption in transit for production deployments
