import pandas as pd 
from sqlalchemy import text
import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts/python"))
)

from credentials import get_connection
engine = get_connection()
query = """
SELECT table_schema, table_name, table_type
FROM information_schema.tables
WHERE table_schema  IN ('raw')
ORDER BY table_schema, table_name
"""
result = pd.read_sql(text(query), engine)
print(result)
for table in result.table_name:
    query = f"""
    SELECT * from raw.{table}
    """
    print(pd.read_sql(text(query), engine))


engine.dispose()