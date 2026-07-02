FROM python:3.12-slim

ARG APP_UID=1000
ARG APP_GID=1000
ARG APP_USER=app

# Add user
COPY helper/setup-user.sh /usr/local/bin/setup-user.sh

RUN chmod +x /usr/local/bin/setup-user.sh \
    && /usr/local/bin/setup-user.sh

# Add console styles
COPY helper/shell-comfort.sh /usr/local/bin/shell-comfort.sh

RUN chmod +x /usr/local/bin/shell-comfort.sh \
    && /usr/local/bin/shell-comfort.sh

# Additional
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        binutils \
        build-essential \
        python3-tk \
        tk \
        zip \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir pyinstaller

WORKDIR /workspace