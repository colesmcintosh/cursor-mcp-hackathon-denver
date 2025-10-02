FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    PORT=8000

WORKDIR /app

# Install dependencies into an isolated virtual environment so the
# image stays small and reproducible.
COPY requirements.txt ./
RUN python -m venv "$VIRTUAL_ENV" \
    && "$VIRTUAL_ENV"/bin/pip install --upgrade pip \
    && "$VIRTUAL_ENV"/bin/pip install --no-cache-dir -r requirements.txt

COPY . .

# Drop privileges to a non-root user for better security when deployed.
RUN useradd --system --home /app appuser \
    && chown -R appuser:appuser /app

USER appuser

# Expose the port (Railway will override PORT env var)
EXPOSE 8000

# Run HTTP server for Railway deployment
CMD ["python", "http_server.py"]
