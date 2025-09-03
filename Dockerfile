FROM python:3.13-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ADD . /app

WORKDIR /app
RUN uv sync

# Instala o cron e cliente PostgreSQL
RUN apt-get update && apt-get install -y cron postgresql-client && rm -rf /var/lib/apt/lists/*

# Tornar entrypoint executável
RUN chmod +x /app/scripts/entrypoint.sh
RUN chmod +x /app/scripts/run_job.sh