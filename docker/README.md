# Docker Layer

## Overview

This project uses a modular Docker Compose structure:

```text
docker/
  compose.yml          # base configuration
  services/            # additional service modules
```

All `*.yml` / `*.yaml` files inside `docker/services/` are automatically loaded by:

```bash
./ops/up.sh
```

⚠️ Do NOT place example files into `services/` unless you want them to run.

---

## Internal Project Network

By default, services can run inside an isolated Docker network:

```yaml
services:
  app:
    image: nginx:alpine
    networks:
      - internal_net

networks:
  internal_net:
    driver: bridge
```

### What this means

- Services can communicate with each other inside the same Compose project.
- Other projects cannot access them directly.
- This is the safest default for isolated development environments.

---

## Shared Network (Cross-Project Communication)

Use a shared Docker network only when one project must communicate with another project.

Example:

```text
project-one/app  →  project-two/api
```

### Step 1 — shared network is prepared by `ops/up.sh`

`./ops/docker/up.sh` checks whether the shared network exists.
If it does not exist, it creates it automatically.
If it already exists, it skips creation.

Default values are stored in project `.env`:

```env
SHARED_NETWORK_NAME=default_shared
AUTO_CREATE_SHARED_NETWORK=1
```

Manual command, if needed:

```bash
docker network create default_shared
```

---

### Step 2 — connect a service to the shared network

```yaml
services:
  app:
    image: nginx:alpine
    networks:
      - internal_net
      - default_shared

networks:
  internal_net:
    driver: bridge

  default_shared:
    external: true
```

---

### Step 3 — define an alias inside the shared network

```yaml
services:
  app:
    image: nginx:alpine
    networks:
      internal_net:
      default_shared:
        aliases:
          - example-app.local

networks:
  internal_net:
    driver: bridge

  default_shared:
    external: true
```

---

## How shared aliases work

Aliases are Docker-network DNS names.

Containers connected to `default_shared` can access the service by alias:

```text
http://example-app.local
```

Important:

- This alias works inside Docker networks.
- It does not automatically work from the host OS browser.
- For browser access from the host, use ports, `/etc/hosts`, reverse proxy, or a gateway later.

---

## Recommended Naming Strategy

Use predictable names:

```text
<project>-<service>.local
```

Examples:

```text
billing-api.local
auth-service.local
frontend.local
```

For shared networks, prefer names that are unique across projects.

---

## Important Notes

- Keep services isolated by default.
- Use shared network only when cross-project communication is required.
- `ops/docker/up.sh` can create the shared network automatically.
- Default shared network name is `default_shared`.
- You can override it for one run: `./ops/docker/up.sh --shared-network my_project_shared`.
- Avoid alias collisions across projects.
- Remember that `ops/docker/up.sh` automatically loads all Compose files from `docker/services/`.

---

## Quick Commands

Start project:

```bash
./ops/up.sh
```

Start only Docker:

```bash
./ops/docker/up.sh
```

Start with a custom shared network name:

```bash
./ops/docker/up.sh --shared-network my_project_shared
```

This overrides `SHARED_NETWORK_NAME` from `.env` only for this run.

Stop project:

```bash
./ops/down.sh
```

Destroy Docker runtime resources:

```bash
./ops/destroy.sh
```

---

## Philosophy

- Simple by default.
- Isolated by default.
- Shared only when needed.
- No hidden magic without documentation.