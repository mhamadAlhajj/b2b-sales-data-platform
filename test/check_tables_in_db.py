from dotenv import load_dotenv
import os
import pandas as pd 
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy import text


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



query = """
SELECT table_schema, table_name, table_type
FROM information_schema.tables
WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY table_schema, table_name
"""
print(pd.read_sql(text(query), engine))

query = """
SELECT * from raw."address"
"""
print(pd.read_sql(text(query), engine))


engine.dispose()