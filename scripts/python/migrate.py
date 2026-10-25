from dotenv import load_dotenv
import os
import hashlib
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from pathlib import Path


load_dotenv()

url = URL.create(
    "postgresql+psycopg2",
    username=os.environ["POSTGRES_USER_DEV"],
    password=os.environ["POSTGRES_PASSWORD_DEV"],
    host="localhost",
    port=int(os.environ["POSTGRES_PORT_DEV"]),
    database=os.environ["POSTGRES_DB_DEV"],
)
engine = create_engine(url)

MIGRATIONS_DIR = Path("./scripts/SQL/migrations")
files = sorted(MIGRATIONS_DIR.glob("V*.sql"))

BOOTSTRAP = files[0]

with engine.begin() as conn:
    conn.exec_driver_sql(BOOTSTRAP.read_text(encoding="utf-8"))

    applied = dict(
        conn.execute(
            text("SELECT file_name, checksum FROM audit.schema_migrations")
        ).all()
    )

    for f in files:
        sql = f.read_text(encoding="utf-8")
        checksum = hashlib.sha256(sql.encode("utf-8")).hexdigest()

        if f.name in applied:
            if applied[f.name] != checksum:
                raise RuntimeError(
                    f"{f.name} was already applied but its content has changed. "
                    "Add a new migration instead of editing an applied one."
                )
            print(f"skip   {f.name}")
            continue

        conn.exec_driver_sql(sql)
        conn.execute(
            text(
                "INSERT INTO audit.schema_migrations (file_name, checksum) "
                "VALUES (:f, :c)"
            ),
            {"f": f.name, "c": checksum},
        )
        print(f"apply  {f.name}")

engine.dispose()
