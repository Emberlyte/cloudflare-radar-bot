FROM python:3.14-alpine

RUN apk add --no-cache gcc musl-dev libffi-dev

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app

RUN adduser -D appuser && chown appuser /app

RUN ln -sf /usr/local/bin/python3.14 /usr/bin/python3

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY --chown=appuser:appuser . .

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

RUN mkdir -p /app/data /app/logs && \
    chown -R appuser:appuser /app/data /app/logs /app/.venv

USER appuser
CMD ["python", "-m", "bot.main"]