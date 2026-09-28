# check=skip=JSONArgsRecommended
# Single-container Reflex deployment for Hugging Face Spaces (Docker SDK).
# Caddy serves the exported frontend and proxies backend routes on one port.
ARG PORT=7860
ARG API_URL

FROM python:3.13-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:0.12 /uv /bin/uv
COPY --from=oven/bun:1 /usr/local/bin/bun /usr/local/bin/bun
ENV UV_COMPILE_BYTECODE=1 UV_NO_CACHE=1 PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY requirements.txt .
RUN uv venv && uv pip install -r requirements.txt

COPY . .

ARG PORT API_URL
RUN --mount=type=cache,target=/root/.bun/install/cache \
    REFLEX_API_URL=${API_URL:-http://localhost:$PORT} reflex export --frontend-only --no-zip

FROM python:3.13-slim

RUN apt-get update -y && apt-get install -y --no-install-recommends redis-server \
    && rm -rf /var/lib/apt/lists/*
COPY --from=caddy:2 /usr/bin/caddy /usr/bin/caddy

ARG PORT
ENV PATH="/app/.venv/bin:$PATH" PORT=$PORT REFLEX_REDIS_URL=redis://localhost PYTHONUNBUFFERED=1

WORKDIR /app
RUN adduser --disabled-password --gecos "" --home /app reflex && chown reflex /app
COPY --chown=reflex --from=builder /app/.venv .venv
COPY --chown=reflex --from=builder /app/.web/backend .web/backend
COPY --from=builder /app/.web/build/client /srv
COPY --chown=reflex . .
USER reflex

EXPOSE $PORT

CMD caddy start --config /app/Caddyfile && \
    redis-server --daemonize yes && \
    exec reflex run --env prod --backend-only
