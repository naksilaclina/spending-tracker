# Finance OS Backend

Django + DRF backend for a personal finance operating system using Supabase Auth and Supabase Postgres.

## Quick start

```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -e .[dev]
copy .env.example .env
python manage.py migrate
python manage.py runserver
```

OpenAPI schema is available at `/api/schema/` and Swagger UI at `/api/docs/`.
