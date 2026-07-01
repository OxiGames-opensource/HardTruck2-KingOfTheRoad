#!/usr/bin/env sh
set -eu

APP_UID="${APP_UID:-1000}"

APP_HOME="$(getent passwd "${APP_UID}" | cut -d: -f6)"

SHELL_COMFORT_FILE="/tmp/oxifabrics-shell-comfort"

cat > "${SHELL_COMFORT_FILE}" <<'COMFORT'
export TERM=xterm-256color

if ls --color=auto >/dev/null 2>&1; then
    alias ls="ls --color=auto"
elif ls -G >/dev/null 2>&1; then
    alias ls="ls -G"
fi

if ls --color=auto >/dev/null 2>&1; then
    alias ll="ls -la --color=auto"
elif ls -G >/dev/null 2>&1; then
    alias ll="ls -la -G"
else
    alias ll="ls -la"
fi

export PS1="\[\033[32m\]\u@\h\[\033[0m\]:\[\033[34m\]\w\[\033[0m\]\$ "
COMFORT

cat "${SHELL_COMFORT_FILE}" >> /root/.profile
cat "${SHELL_COMFORT_FILE}" >> "${APP_HOME}/.profile"

if [ -x /bin/bash ]; then
    cat "${SHELL_COMFORT_FILE}" >> /root/.bashrc
    cat "${SHELL_COMFORT_FILE}" >> "${APP_HOME}/.bashrc"
fi

rm -f "${SHELL_COMFORT_FILE}"