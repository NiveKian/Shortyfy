# Build stage
FROM python:3.13-slim-bookworm AS builder

# Copy uv binary
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /bin/uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /app

# Copy only dependency files first
COPY uv.lock pyproject.toml ./

# Install dependencies
RUN uv sync --frozen --no-install-project

# Copy the app folder
COPY app ./app

# Final image
FROM python:3.13-slim-bookworm AS final

WORKDIR /app
COPY --from=builder /app /app

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
