# from app.database.database import async_session
from sqlalchemy import select

from app.database.database import SessionLocal
from app.models import Ministerie


def get_many() -> list[Ministerie]:
    with SessionLocal() as session:
        return list(
            (session.scalars(select(Ministerie).order_by(Ministerie.Naam))).all()
        )
