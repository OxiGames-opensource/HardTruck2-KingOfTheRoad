FROM ubuntu:24.04

ARG APP_UID=1000
ARG APP_GID=1000
ARG APP_USER=app

ARG GHIDRA_VERSION=12.1.2
ARG GHIDRA_DATE=20260605
ARG GHIDRA_BUILD=Ghidra_${GHIDRA_VERSION}_build
ARG GHIDRA_ZIP=ghidra_${GHIDRA_VERSION}_PUBLIC_${GHIDRA_DATE}.zip
ARG GHIDRA_URL=https://github.com/NationalSecurityAgency/ghidra/releases/download/${GHIDRA_BUILD}/${GHIDRA_ZIP}

ENV DEBIAN_FRONTEND=noninteractive

# Add user
COPY helper/setup-user.sh /usr/local/bin/setup-user.sh

RUN chmod +x /usr/local/bin/setup-user.sh \
    && /usr/local/bin/setup-user.sh

# Add console styles
COPY helper/shell-comfort.sh /usr/local/bin/shell-comfort.sh

RUN chmod +x /usr/local/bin/shell-comfort.sh \
    && /usr/local/bin/shell-comfort.sh

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    wget \
    unzip \
    file \
    binutils \
    openjdk-21-jdk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:/opt/ghidra/support:${PATH}"

RUN wget -O /tmp/ghidra.zip "${GHIDRA_URL}" \
    && unzip /tmp/ghidra.zip -d /opt \
    && rm /tmp/ghidra.zip \
    && mv /opt/ghidra_* /opt/ghidra \
    && chown -R ${APP_UID}:${APP_GID} /opt/ghidra

WORKDIR /workspace
USER ${APP_USER}