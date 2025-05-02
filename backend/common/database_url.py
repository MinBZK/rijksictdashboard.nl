import urllib.parse

from dotenv import load_dotenv

from app.config.env import settings

load_dotenv()


def get_database_url(use_async: bool = False) -> str:
    driver = "postgresql+asyncpg" if use_async else "postgresql"
    USERNAME = settings.POSTGRES_USER
    PASSWORD = urllib.parse.quote_plus(settings.POSTGRES_PASSWORD)
    HOST = settings.POSTGRES_SERVER
    SCHEMA = settings.POSTGRES_DB
    PORT = settings.POSTGRES_PORT
    connection_string = f"{driver}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{SCHEMA}"
    return connection_string
