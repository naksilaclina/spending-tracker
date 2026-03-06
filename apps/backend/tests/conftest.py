import os

os.environ.setdefault("DJANGO_SECRET_KEY", "test")
os.environ.setdefault("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/finance_os")
os.environ.setdefault("SUPABASE_URL", "https://example.supabase.co")
