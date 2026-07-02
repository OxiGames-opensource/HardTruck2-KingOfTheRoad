#!/usr/bin/env bash

set -euo pipefail

docker compose exec release-builder \
    bash -lc 'cd tools/release-builder && ./BuildLinux.sh'