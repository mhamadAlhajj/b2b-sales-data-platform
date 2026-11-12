import hashlib
import uuid
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
from sqlalchemy import text
from credentials import get_connection


engine = get_connection()

source_path = Path('./dataset/data.xlsx')
file_checksum = hashlib.sha256(source_path.read_bytes()).hexdigest()
excel_sheets = pd.read_excel(source_path, sheet_name=None, dtype=str)

run_id = str(uuid.uuid4())

LOG_SQL = text("""
    INSERT INTO audit.load_log (
        run_id, source_file, source_sheet, target_table, file_checksum,
        rows_read, rows_loaded, status, error_message, started_at
    ) VALUES (
        :run_id, :source_file, :source_sheet, :target_table, :file_checksum,
        :rows_read, :rows_loaded, :status, :error_message, :started_at
    )
""")

failed = []
for sheet_name, df in excel_sheets.items():
    table = sheet_name.lower()
    started_at = datetime.now(timezone.utc)
    rows_loaded = None
    status = "success"
    error_message = None
    try:
        with engine.begin() as conn:
            df = df.assign(
                _source_sheet=sheet_name,
                _loaded_at=pd.Timestamp.now(tz="UTC"),
            )
            df.to_sql(table, conn, schema="raw", if_exists="replace", index=False)
            rows_loaded = conn.execute(text(f'SELECT count(*) FROM raw."{table}"')).scalar()
            assert rows_loaded == len(df), f"Row count mismatch in {table}"
    except Exception as e:
        status = "failed"
        error_message = str(e)
        failed.append(sheet_name)

    with engine.begin() as conn:
        conn.execute(LOG_SQL, {
            "run_id": run_id,
            "source_file": source_path.name,
            "source_sheet": sheet_name,
            "target_table": f"raw.{table}",
            "file_checksum": file_checksum,
            "rows_read": len(df),
            "rows_loaded": rows_loaded,
            "status": status,
            "error_message": error_message,
            "started_at": started_at,
        })
    print(f"{status:7} {sheet_name} ({len(df)} rows read)")

engine.dispose()

if failed:
    raise SystemExit(f"Load failed for sheets: {', '.join(failed)}")