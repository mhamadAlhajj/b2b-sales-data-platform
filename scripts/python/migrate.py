import hashlib
from sqlalchemy import  text
from pathlib import Path
from credentials import get_connection


engine = get_connection()

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
