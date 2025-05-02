import pytest
from sqlalchemy import text

from app.middleware import get_db
from common.database_url import get_database_url


def test_get_db():
    """Test if the db is reachable"""
    db = next(get_db())
    assert db
    assert db.execute(text("SELECT 1"))


@pytest.mark.parametrize("use_async", [True, False])
def test_database_url(use_async: bool):
    database_url = get_database_url(use_async=use_async)
    assert database_url is not None
