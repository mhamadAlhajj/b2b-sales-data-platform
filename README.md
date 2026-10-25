# B2B Sales Data Modeling (PostgreSQL, dbt, Power BI)

An end-to-end data engineering project that turns a messy Excel export of B2B sales
data into a documented, tested, and reproducible analytics platform.

## What it does
1. **Ingest:** Python (pandas, SQLAlchemy) loads every Excel sheet unchanged into the
   `raw` schema of a PostgreSQL database.
2. **Understand:** the data is profiled, and an ERD (conceptual and logical) documents
   the entities and relationships.
3. **Clean and normalize:** dbt builds a trusted, normalized `core` schema, with
   data quality tests and a quarantine for rejected records.
4. **Model for analytics:** dbt builds a star schema (facts and dimensions) in the
   `dwh` schema.
5. **Report:** a Power BI report on top of `dwh` answers the business questions
   (sales vs targets, profitability, delivery speed, payments, marketing, stock, and more).
6. **Release:** the result is promoted from development to production.

## Project structure
```text
.
├── compose.yaml              # development and production PostgreSQL servers
├── dataset/                  # source Excel file
├── docker-postgres-init/     # database init script
├── notebook files/           # step-by-step notebooks
├── scripts/
│   ├── python/               # migration runner, loaders
│   └── SQL/migrations/       # numbered SQL migrations (V001__*.sql, ...)
├── test/                     # database checks
├── .env.example
├── requirements.txt
└── README.md
```

## Prerequisites
- Python 3.14
- Docker (PostgreSQL 18 image)

## Setup
1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in the values.

## How to run
Run from the project root:
```bash
python scripts/python/migrate.py
python scripts/python/load_raw.py
```

## Architecture
Excel -> `raw` -> `core` -> `dwh` -> Power BI

| Schema | Purpose | Built by |
|---|---|---|
| raw | Source data exactly as received | Python loader |
| core | Cleaned, normalized, trusted data | dbt |
| dwh | Star schema for analytics | dbt |
| audit | Migration tracking and run logs | SQL migrations and the pipeline runner |

## Engineering practices
- Two PostgreSQL servers in Docker: development and production.
- Production is protected (read-only) until the release.
- SQL migrations create the schemas and the `audit` tables. The loader creates the `raw` tables.
- `core` and `dwh` are built only by dbt, with tests and generated documentation.
- Secrets are never committed to Git.