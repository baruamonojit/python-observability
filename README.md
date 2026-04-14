# Python Observability Demo

A demonstration project showcasing structured logging with Python and the PLG (Promtail + Loki + Grafana) stack for observability.

## Overview

This project demonstrates how to emit structured JSON logs from a Python application and ship them to Loki for visualization in Grafana. It provides a complete observability setup using Docker containers.

## Architecture

The data flow follows this pattern:
- **Python App** (stdout JSON logs) → **Docker Logging Driver** (json-file) → **Promtail** (docker socket discovery) → **Loki** (ingest & index) → **Grafana** (visualize dashboards)

## Key Components

- `app.py`: Python application emitting structured JSON log lines using a custom JsonFormatter
- `Dockerfile`: Container image for the hello-world application
- `docker-compose.yml`: Orchestrates the full stack (app, promtail, loki, grafana)
- `loki/config.yml`: Loki server configuration
- `promtail-config.yml`: Promtail configuration for log scraping
- `hello-world.json`: Sample Grafana dashboard export

## Prerequisites

- Docker and Docker Compose
- Python 3.12+ (for local development)

## Quick Start

### Full Stack with Docker Compose

To run the complete observability stack:

```bash
docker compose up --build
```

This starts all services: the Python app, Promtail, Loki, and Grafana.

### Run App Only with Compose

To run just the app service while still using the compose network:

```bash
docker compose up --build hello-world
```

### Direct Python Execution

For local development:

```bash
python app.py
```

### Single Docker Image

Build and run the app in a standalone container:

```bash
docker build -t hello-world .
docker run --rm -e PYTHONUNBUFFERED=1 --name hello-world-app hello-world
```

## Configuration

### Structured Logging

The application uses a custom `JsonFormatter` that emits logs with these fields:
- `timestamp`: ISO format timestamp
- `level`: Log level (INFO, ERROR, etc.)
- `service`: Service name
- `message`: Log message
- `logger`: Logger name
- `pid`: Process ID

Additional metadata is merged from `record.extra` (e.g., `iteration`, `uptime_seconds`).

### Promtail Discovery

Containers are labeled for Promtail scraping:
```yaml
labels:
  logging: "promtail"
```

Promtail's `docker_sd_configs` filters on this label.

### Docker Logging

Uses `json-file` driver with rotation options:
- `max-size`: Maximum log file size
- `max-file`: Maximum number of log files

## Accessing Services

- **Grafana**: http://localhost:3000 (admin/admin)
- **Loki**: http://localhost:3100
- **Promtail**: Internal service for log scraping

## Development

### Adding New Services

When adding containers that should be scraped by Promtail:
1. Add the `logging: "promtail"` label to the service
2. Ensure service names match Promtail's filters

### Log Flushing

`PYTHONUNBUFFERED=1` is set to ensure logs appear immediately in Docker logs and Promtail without buffering.

## Testing

No automated tests are currently configured. For future test setup:
- Use pytest for unit tests
- Example: `pytest tests/test_file.py::test_name`
- Run by expression: `pytest -k <expr>`

## License

This project is provided as-is for demonstration purposes.
