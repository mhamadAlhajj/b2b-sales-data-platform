from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

def get_connection():
    load_dotenv()
    db_name = os.getenv('POSTGRES_DB_DEV')
    postgres_user = os.getenv('POSTGRES_USER_DEV')
    postgres_password = os.getenv('POSTGRES_PASSWORD_DEV')
    postgres_port = os.getenv('POSTGRES_PORT_DEV')

    url = URL.create(
        "postgresql+psycopg2",
        username=postgres_user,
        password=postgres_password,
        host="localhost",
        port=int(postgres_port),
        database=db_name,
    )
    engine = create_engine(url)
    return engine