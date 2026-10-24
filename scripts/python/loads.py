from dotenv import load_dotenv
import os
import pandas as pd 
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy import text
from pathlib import Path


load_dotenv()
db_name = os.getenv('POSTGRES_DB_DEV')
postgres_user = os.getenv('POSTGRES_USER_DEV')
postgres_password = os.getenv('POSTGRES_PASSWORD_DEV')
postgres_port = os.getenv('POSTGRES_PORT_DEV')

url = URL.create(
    "postgresql+psycopg2",
    username=os.environ["POSTGRES_USER_DEV"],
    password=os.environ["POSTGRES_PASSWORD_DEV"],
    host="localhost",
    port=int(os.environ["POSTGRES_PORT_DEV"]),
    database=os.environ["POSTGRES_DB_DEV"],
)
engine = create_engine(url)

excel_sheets = pd.read_excel('./dataset/data.xlsx' , sheet_name=None ,  dtype=str)

migration = Path("./scripts/SQL/migrations/V001__create_schemas.sql")
sql = migration.read_text(encoding="utf-8")

with engine.begin() as conn:
    conn.exec_driver_sql(sql)
    for sheet_name, df in excel_sheets.items():
        table = sheet_name.lower()
        df = df.assign(
            _source_sheet=sheet_name,
            _loaded_at=pd.Timestamp.now(tz="UTC"),
        )
        df.to_sql(table, conn, schema="raw", if_exists="replace", index=False)
        n = conn.execute(text(f'SELECT count(*) FROM raw."{table}"')).scalar()
        assert n == len(df), f"Row count mismatch in {table}"

engine.dispose()