# Docker Compose Demo — Multi-Container QE Infrastructure

## What This Is
A complete working example of 3 Docker containers working together:
- **db** — PostgreSQL database (seeded with test data)
- **api** — Flask mock API server (CRUD for products)
- **test-runner** — pytest suite that validates the API

## Prerequisites
- Docker Desktop installed (https://www.docker.com/products/docker-desktop/)

## Run Everything (One Command)
```bash
docker compose up --build --abort-on-container-exit
```

## View the Test Report
After tests finish, open: `reports/report.html`

## Useful Commands
```bash
# Run tests only (after first build)
docker compose up test-runner

# Rebuild everything from scratch
docker compose build --no-cache

# Tear down everything
docker compose down -v

# Check what's running
docker compose ps

# See logs from a specific container
docker compose logs api
docker compose logs db
```

## Troubleshooting

### Port Already in Use (5432 or 5050)
If you see "port is already allocated" errors:

**Port 5432 (PostgreSQL)**
- Stop any local PostgreSQL service: `brew services stop postgresql`
- Or, modify `docker-compose.yml` line 28 to use a different host port, e.g. `"5433:5432"`

**Port 5050 (Flask API)**
- On macOS, this may conflict with AirPlay Receiver. Either:
  1. Disable AirPlay Receiver in System Settings → General → AirDrop & Handoff, or
  2. Modify `docker-compose.yml` line 39 to use a different host port, e.g. `"5051:5000"` (the container port stays 5000, so internal tests still work)

**Other containers stuck/won't clean up**
```bash
# Force remove all containers and networks
docker compose down -v
docker container prune -f
```

## Architecture
```
┌──────────────┐     ┌──────────────────┐     ┌──────────────┐
│   db         │     │   api            │     │  test-runner  │
│  PostgreSQL  │◄────│  Flask API       │◄────│   pytest      │
│  5432        │     │  5050 (host)     │     │               │
│  (container) │     │  5000 (container)│     │               │
└──────────────┘     └──────────────────┘     └──────────────┘
     Container 1          Container 2            Container 3
```

**Port Mappings:**
- **db** — 5432:5432 (PostgreSQL, container-only — no host access needed)
- **api** — 5050:5000 (Flask, host:container — use `localhost:5050` from your browser/curl for debugging)
- **test-runner** — no host ports (reaches api via Docker DNS at `http://api:5000`)
