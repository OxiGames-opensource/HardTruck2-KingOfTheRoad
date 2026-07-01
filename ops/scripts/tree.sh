#!/usr/bin/env bash

set -euo pipefail

SERVICE="${1:-ghidra}"
TARGET_DIR="${2:-.}"
DEPTH="${4:-4}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$PROJECT_ROOT"

ENV_FILE=".env"
BASE_COMPOSE_FILE="docker/compose.yml"
SERVICE_COMPOSE_FILE="docker/services/${SERVICE}/compose.yml"

echo "[INFO] Project:         $PROJECT_ROOT"

if [ ! -f "$ENV_FILE" ]; then
    echo "[FIX] Environment file not found: $ENV_FILE"
    echo "[INFO] Create it from .env.example:"
    echo "       cp .env.example .env"
    exit 1
fi

if [ ! -f "$BASE_COMPOSE_FILE" ]; then
    echo "[FIX] Base Docker Compose file not found:"
    echo "       $BASE_COMPOSE_FILE"
    exit 1
fi

if [ ! -f "$SERVICE_COMPOSE_FILE" ]; then
    echo "[FIX] Service Docker Compose file not found:"
    echo "       $SERVICE_COMPOSE_FILE"
    exit 1
fi

if ! docker compose \
    --env-file "$ENV_FILE" \
    -f "$BASE_COMPOSE_FILE" \
    -f "$SERVICE_COMPOSE_FILE" \
    config --services | grep -qx "$SERVICE"; then

    echo "[FIX] Docker Compose service not found: $SERVICE"
    echo
    echo "[INFO] Available services:"
    docker compose \
        --env-file "$ENV_FILE" \
        -f "$BASE_COMPOSE_FILE" \
        -f "$SERVICE_COMPOSE_FILE" \
        config --services || true

    exit 1
fi

echo "[INFO] Env file:        $ENV_FILE"
echo "[INFO] Base compose:    $BASE_COMPOSE_FILE"
echo "[INFO] Service compose: $SERVICE_COMPOSE_FILE"
echo "[INFO] Service:         $SERVICE"
echo "[INFO] Target:          $TARGET_DIR"
echo "[INFO] Depth:           $DEPTH"
echo

docker compose \
    --env-file "$ENV_FILE" \
    -f "$BASE_COMPOSE_FILE" \
    -f "$SERVICE_COMPOSE_FILE" \
    exec "$SERVICE" bash -lc "

        if ! command -v tree >/dev/null 2>&1; then
            echo '[FIX] tree command not found inside container'
            exit 1
        fi

        cd '$TARGET_DIR'
        tree -a -L '$DEPTH'
    "