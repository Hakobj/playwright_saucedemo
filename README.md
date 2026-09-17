# playwright_saucedemo

A full-stack QE training project covering **UI**, **API**, and **Database** testing — all runnable locally with pytest or fully containerized with Docker / Docker Compose.

## Prerequisites

- **Git**
- **Python 3.11+** — only needed to run the UI tests locally
- **Docker Desktop** — must be running before any `docker` / `docker compose` command

## Quick Start

**UI tests (local):**

```bash
git clone https://github.com/Hakobj/playwright_saucedemo.git
cd playwright_saucedemo
python -m venv .venv
.venv\Scripts\activate            # PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m playwright install chromium
pytest --html=reports/report.html --self-contained-html
```

**Full API + DB stack (Docker, no local setup needed):**

```bash
cd sql-testing-demo
docker compose up --build --abort-on-container-exit
```

A green `passed` summary means success. Open the HTML report afterwards:
- UI/API: `reports/report.html`
- API+DB: `sql-testing-demo/reports/report.html`

## Project Overview

| Layer | What it tests | Tools | Location |
|-------|---------------|-------|----------|
| **UI tests** | [saucedemo.com](https://www.saucedemo.com) — login, inventory, cart | Playwright + pytest, Page Object Model | [tests/](tests/), [pages/](pages/) |
| **API tests (mock)** | JSONPlaceholder REST API — CRUD, headers | Playwright APIRequestContext | [tests/test_api_get.py](tests/test_api_get.py), [tests/test_api_crud.py](tests/test_api_crud.py), [tests/test_api_headers.py](tests/test_api_headers.py) |
| **API + DB tests** | Mock Flask Product API backed by PostgreSQL | pytest, requests, psycopg2, Docker Compose | [sql-testing-demo/](sql-testing-demo/) |

## Project Structure

```
playwright_saucedemo/
├── conftest.py                  # Root fixtures: page objects, --env option, auth state, API context
├── Dockerfile                   # Containerized Playwright test runner
├── requirements.txt             # pytest-playwright, pytest-xdist, pytest-html
├── data/
│   ├── models.py                # User / Product dataclasses (frozen)
│   └── test_data.py             # Named users & products (no magic strings)
├── pages/                       # Page Object Model
│   ├── login_page.py            # LoginPage — locators + actions + queries
│   └── inventory_page.py        # InventoryPage — cart badge, add-to-cart
├── tests/                       # UI + mock API tests
│   ├── test_login.py            # Login flows
│   ├── test_login_matrix.py     # Parametrized login scenarios
│   ├── test_add_to_cart.py      # Cart badge / add-to-cart
│   ├── test_authenticated.py    # Reuses saved auth state
│   ├── test_problem_user.py     # problem_user regression scenarios
│   ├── test_product_matrix.py   # Parametrized product/price checks
│   └── test_api_*.py            # API tests against JSONPlaceholder
├── .github/workflows/
│   └── docker-tests.yml         # CI: runs docker compose, uploads HTML report
└── sql-testing-demo/            # ── API + DB testing sub-project ──
    ├── docker-compose.yml       # 3-container stack: db, api, test-runner
    ├── SQL_CHEAT_SHEET.md       # SQL reference for the tests
    ├── app/
    │   ├── server.py            # Flask Product API + PostgreSQL (seeded)
    │   ├── Dockerfile
    │   └── requirements.txt     # flask, psycopg2-binary
    ├── tests/
    │   ├── conftest.py          # api_ready / api_url / db_connection / db_cursor fixtures
    │   ├── test_product_api.py  # API-level tests (GET/POST/PUT/DELETE, lifecycle)
    │   ├── test_database.py     # DB-level tests (SQL basics, receipts, integrity)
    │   ├── Dockerfile
    │   └── requirements.txt     # pytest, requests, pytest-html, psycopg2-binary
    └── reports/                 # HTML test report (mounted from container)
```

---

## 1. UI Tests (Playwright)

Tests against [saucedemo.com](https://www.saucedemo.com) using the **Page Object Model**:

- **[pages/login_page.py](pages/login_page.py)** — locators are named once (`[data-test='username']` etc.), tests call domain actions like `login_as(user)`.
- **[pages/inventory_page.py](pages/inventory_page.py)** — domain queries like `cart_count()` and `is_loaded()` keep selectors out of tests.
- **[data/models.py](data/models.py)** — frozen `User` / `Product` dataclasses so test data can't mutate mid-run.
- **[conftest.py](conftest.py)** — provides `login_page` / `inventory_page` fixtures, a `--env` CLI option (`dev | staging | prod`), and **session-scoped auth state**: logs in once, saves `.auth/standard.json`, and reuses it via `storage_state`. Tests marked `@pytest.mark.no_auth` start logged out.

### Run UI tests locally

```bash
pip install -r requirements.txt
python -m playwright install chromium

pytest                                          # all UI + mock API tests
pytest tests/test_login.py -v                   # one file
pytest --env staging                            # pick an environment
pytest -n auto                                  # parallel with pytest-xdist
pytest --html=reports/report.html --self-contained-html
```

### Run UI tests in Docker

```bash
docker build -t saucedemo-tests .
docker run --rm -v ${PWD}/reports:/app/reports saucedemo-tests
```

---

## 2. API Tests

Two flavors of API testing:

**Mock API (JSONPlaceholder)** — [tests/test_api_get.py](tests/test_api_get.py), [tests/test_api_crud.py](tests/test_api_crud.py), [tests/test_api_headers.py](tests/test_api_headers.py) use Playwright's `APIRequestContext` (the `api` fixture in [conftest.py](conftest.py)) for GET/POST/PUT/DELETE and header validation.

**Flask Product API (sql-testing-demo)** — [sql-testing-demo/app/server.py](sql-testing-demo/app/server.py) is a real REST API backed by PostgreSQL, seeded with 4 Sauce Labs products:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check (verifies DB connectivity) |
| `/api/products` | GET | List all products |
| `/api/products/<id>` | GET | Get one product (404 if missing) |
| `/api/products` | POST | Create (requires `name` + `price`, else 400) |
| `/api/products/<id>` | PUT | Update a product |
| `/api/products/<id>` | DELETE | Delete a product |

[sql-testing-demo/tests/test_product_api.py](sql-testing-demo/tests/test_product_api.py) covers status codes, response schemas, parametrized price checks, validation errors (400), and a full **create → read → update → delete → verify-gone** lifecycle.

---

## 3. Database Tests

[sql-testing-demo/tests/test_database.py](sql-testing-demo/tests/test_database.py) connects **directly to PostgreSQL** (bypassing the API) via the `db_connection` / `db_cursor` fixtures in [sql-testing-demo/tests/conftest.py](sql-testing-demo/tests/conftest.py).

Four layers of DB testing:

1. **SQL Basics** — `SELECT`, specific columns, `WHERE`, comparisons, `COUNT`, `ORDER BY`, boolean filters.
2. **API + DB validation ("receipts" pattern)** — call the API, then verify the database directly: the API may *say* 201 Created, but these tests confirm the row *actually exists* (and that deletes really remove it, and API counts match `COUNT(*)`).
3. **Data integrity** — unique IDs, no empty names, positive prices, no NULL `in_stock`.
4. **Direct writes** — `INSERT` / `UPDATE` / `DELETE` from Python with cleanup after each test.

> PostgreSQL returns `Decimal` for `NUMERIC` columns — compare against `Decimal("29.99")`, not `29.99`. See [sql-testing-demo/SQL_CHEAT_SHEET.md](sql-testing-demo/SQL_CHEAT_SHEET.md) for more.

---

## 4. Docker Compose (sql-testing-demo)

[sql-testing-demo/docker-compose.yml](sql-testing-demo/docker-compose.yml) runs a 3-container stack:

```
┌─────────────┐     ┌─────────────┐     ┌──────────────┐
│     db      │     │     api     │     │  test-runner  │
│  PostgreSQL │◄────│  Flask API  │◄────│    pytest     │
│  Port 5432  │     │  Port 5000  │     │              │
└──────┬──────┘     └─────────────┘     └──────┬───────┘
       │                                       │
       └───────────────────────────────────────┘
          test-runner ALSO connects directly to DB
```

- **db** — `postgres:16-alpine` with a `pg_isready` healthcheck.
- **api** — Flask app; waits for a healthy DB, then creates + seeds the `products` table.
- **test-runner** — runs `pytest -vs --html=/tests/reports/report.html`; has both `API_URL` and DB credentials so it can test through the API *and* behind it. Reports are written to [sql-testing-demo/reports/](sql-testing-demo/reports/) via a volume mount.

### Run the full stack

```bash
cd sql-testing-demo
docker compose up --build --abort-on-container-exit
```

The `--abort-on-container-exit` flag shuts everything down when the test-runner finishes. Open [sql-testing-demo/reports/report.html](sql-testing-demo/reports/report.html) afterwards for the HTML report.

### Practice SQL manually

With the stack running (omit `--abort-on-container-exit`):

```bash
docker compose exec db psql -U testuser -d testdb
```

```sql
SELECT * FROM products;
SELECT name, price FROM products WHERE price > 20;
SELECT COUNT(*) FROM products;
\q
```

---

## CI/CD (GitHub Actions)

[.github/workflows/docker-tests.yml](.github/workflows/docker-tests.yml) runs on every push and PR to `main`:

1. Checks out the repo.
2. Runs `docker compose up --build --abort-on-container-exit` in `sql-testing-demo`.
3. Uploads `sql-testing-demo/reports/` as a **test-report** artifact (even on failure).

## Test Reports

Both suites use `pytest-html` self-contained reports:

- UI/API: `reports/report.html`
- sql-testing-demo: `sql-testing-demo/reports/report.html`