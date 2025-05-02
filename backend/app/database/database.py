from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool

from common.database_url import get_database_url

engine = create_engine(get_database_url(use_async=False), pool_size=15)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# add poolclass=NullPool to prevent asyncio errors when running tests
async_engine = create_async_engine(get_database_url(use_async=True), poolclass=NullPool)
async_session = async_sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, expire_on_commit=False
)


Base = declarative_base()
