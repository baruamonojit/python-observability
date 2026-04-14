Repository-specific Copilot instructions

1) Build, run, test, and lint commands (what exists)

- Run the app locally (direct Python):
  python app.py

- Build and run with Docker (single image):
  docker build -t hello-world .
  docker run --rm -e PYTHONUNBUFFERED=1 --name hello-world-app hello-world

- Full stack (Promtail + Loki + Grafana + app) using Docker Compose:
  docker compose up --build
  # To run only the app service with compose (still uses compose network):
  docker compose up --build hello-world

- Tests / Lint: None configured in this repo.
  If tests are added using pytest, run a single test like:
  pytest tests/test_file.py::test_name
  Or run by expression: pytest -k <expr>
  If a linter (e.g., flake8/ruff) is added, invoke its CLI directly (not present now).

2) High-level architecture (big picture)

- Purpose: PLG (Promtail + Loki + Grafana) demo that emits structured JSON logs from a tiny Python app and ships them to Loki for visualization in Grafana.

- Data flow:
  hello-world app (stdout JSON logs) --> Docker logging driver (json-file) --> Promtail (docker socket discovery) --> Loki (ingest & index) --> Grafana (visualize dashboards)

- Key files implementing the flow:
  - app.py            : emits structured JSON log lines (custom JsonFormatter)
  - Dockerfile        : image for the hello-world app (python:3.12-slim)
  - docker-compose.yml: composes services: hello-world, promtail, loki, grafana
  - loki/config.yml   : Loki server config (mounted into container)
  - hello-world.json  : Grafana dashboard export (sample dashboards)

- Expectations (compose mounts):
  - Promtail config expected at ./promtail/config.yml (docker-compose mounts it)
  - Grafana provisioning expected at ./grafana/provisioning (compose mounts it)
  These may be provided externally (not present in the repo root).

3) Key conventions (repo-specific patterns)

- Structured logging format:
  app.py uses a JsonFormatter that emits JSON with fields: timestamp, level, service, message, logger, pid. Extra metadata is merged from record.extra (e.g., iteration, uptime_seconds).

- Immediate log flushing:
  PYTHONUNBUFFERED=1 is set in Dockerfile and compose env to ensure logs appear in docker logs and Promtail without buffering.

- Promtail discovery label:
  Containers intended to be scraped by Promtail are labelled in docker-compose.yml with:
    labels:
      logging: "promtail"
  Promtail's docker_sd_configs filters on this label — keep it when adding services to be scraped.

- Docker logging driver and options:
  The compose file uses the json-file driver with rotation options (max-size, max-file) — keep these if log rotation is desired in dev/testing.

- Healthchecks & depends_on:
  Compose uses a healthcheck for Loki and depends_on to ensure Promtail/Grafana wait for Loki readiness.

4) AI assistant / other assistant configs discovered

- No Copilot/assistant rule files detected in repository root matching: CLAUDE.md, .cursorrules, AGENTS.md, .windsurfrules, CONVENTIONS.md, AIDER_CONVENTIONS.md, .clinerules. If you add any of these, incorporate important rules into this file.

5) Quick notes for future changes (short & actionable)

- If adding tests, choose pytest and add simple invocation (pytest -q). Example single-test command shown above.
- If adding linting, include a config (pyproject.toml or .flake8) and add a Makefile or scripts/entrypoint for common commands.
- When adding new containers that should be scraped, add the "logging: \"promtail\"" label and ensure the service name/labels match promtail filters.

---

Created by Copilot CLI analysis on 2026-04-14. Edit to expand any section (e.g., include CI commands, test frameworks, or real promtail/grafana configs).
