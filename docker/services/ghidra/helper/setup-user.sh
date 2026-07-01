#!/usr/bin/env sh
set -eu

APP_USER="${APP_USER:-app}"
APP_UID="${APP_UID:-1000}"
APP_GID="${APP_GID:-1000}"

APP_SHELL="/bin/sh"

if [ -x /bin/bash ]; then
    APP_SHELL="/bin/bash"
fi

if ! getent group "${APP_GID}" >/dev/null 2>&1; then
    if command -v groupadd >/dev/null 2>&1; then
        groupadd -g "${APP_GID}" "${APP_USER}"
    elif command -v addgroup >/dev/null 2>&1; then
        addgroup -g "${APP_GID}" "${APP_USER}"
    else
        echo "[ERR] No supported group creation command found"
        exit 1
    fi
fi

if ! getent passwd "${APP_UID}" >/dev/null 2>&1; then
    if command -v useradd >/dev/null 2>&1; then
        useradd -m -u "${APP_UID}" -g "${APP_GID}" -s "${APP_SHELL}" "${APP_USER}"
    elif command -v adduser >/dev/null 2>&1; then
        adduser -D -u "${APP_UID}" -G "${APP_USER}" -s "${APP_SHELL}" "${APP_USER}"
    else
        echo "[ERR] No supported user creation command found"
        exit 1
    fi
fi

APP_HOME="$(getent passwd "${APP_UID}" | cut -d: -f6)"

mkdir -p "${APP_HOME}"
chown "${APP_UID}:${APP_GID}" "${APP_HOME}"

APP_WWW_DIR="${APP_HOME}/www"

mkdir -p "${APP_WWW_DIR}"
chown "${APP_UID}:${APP_GID}" "${APP_WWW_DIR}"