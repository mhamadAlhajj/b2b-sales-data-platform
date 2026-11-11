import pandas as pd 
from sqlalchemy import text
import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts/python"))
)
from credentials import get_connection

engine = get_connection()
address_query = """
    select "Street" , count(distinct "CityName") 
    from raw.address
    group by "Street"
    having count(distinct "CityName") > 1
 """
print(pd.read_sql(text(address_query), engine))
