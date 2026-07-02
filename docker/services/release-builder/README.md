# Docker service: release-builder

This folder contains a Docker Compose service module for OxiFabrics.

## Files

```text
docker/services/release-builder/
├── compose.yml
├── Dockerfile
├── README.md
└── helper/
    ├── setup-user.sh
    └── shell-comfort.sh
```

## How it works

The main Docker runner should load:

```text
docker/compose.yml
docker/services/*/compose.yml
```

This service can be started together with the project by:

```bash
./ops/docker/up.sh
```

## Dockerfile

Base image:

```Dockerfile
FROM python:3.12-slim
```

Example:

```Dockerfile
FROM node:22-alpine

RUN npm install -g gulp-cli

WORKDIR /app
```

## Helper scripts

### setup-user.sh

Creates a container user matching the host user.

Purpose:

- avoid root-owned files
- improve bind mount experience
- provide normal shell user inside containers

### shell-comfort.sh

Configures interactive shell helpers.

Current features:

- TERM=xterm-256color
- ls alias
- ll alias
- colored prompt (when supported)

## Common Dockerfile commands

### COPY

Copy files from your service folder into the image:

```Dockerfile
COPY ./config.conf /etc/example/config.conf
```

### ADD

Similar to COPY, but can also unpack archives and fetch remote URLs.

Prefer COPY unless ADD is really needed.

```Dockerfile
ADD ./archive.tar.gz /opt/app/
```

### RUN

Run commands while building the image:

```Dockerfile
RUN apk add --no-cache bash git
RUN npm install -g gulp-cli
```

### WORKDIR

Set the working directory inside the container:

```Dockerfile
WORKDIR /app
```

### CMD

Default command when the container starts:

```Dockerfile
CMD ["node", "server.js"]
```

## Notes

- Keep service-specific files inside this folder.
- Keep shared project logic in `docker/compose.yml`.
- Helper scripts should remain small and focused.
- Avoid hidden magic. Explicit configuration is preferred.