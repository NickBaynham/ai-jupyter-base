FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PDM_USE_VENV=1 \
    PIP_NO_CACHE_DIR=1

RUN pip install --no-cache-dir pdm

WORKDIR /app

COPY pyproject.toml pdm.lock README.md ./
COPY src ./src
COPY docker/jupyter-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN pdm sync -G notebook

EXPOSE 8888

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
  CMD python -c "import socket; s=socket.create_connection(('127.0.0.1',8888),2); s.close()"

ENTRYPOINT ["/entrypoint.sh"]
