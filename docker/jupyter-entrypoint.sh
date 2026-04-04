#!/bin/sh
set -e
cd /app
# Ensure the local package and notebook extras match the mounted workspace.
pdm sync -G notebook

if [ -n "$JUPYTER_LAB_TOKEN" ]; then
  TOKEN_ARGS="--ServerApp.token=${JUPYTER_LAB_TOKEN}"
else
  # Local Docker only: no token. Do not expose this pattern to the public internet.
  TOKEN_ARGS="--ServerApp.token= --ServerApp.password="
fi

exec pdm run jupyter lab \
  --ip=0.0.0.0 \
  --port=8888 \
  --no-browser \
  --notebook-dir=notebooks \
  ${TOKEN_ARGS} \
  --ServerApp.allow_origin="*"
