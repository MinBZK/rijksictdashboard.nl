import datetime

from sqlalchemy import text

from app.database.database import SessionLocal


def get_laatste_wijziging() -> datetime.datetime | None:
    query = """
        select max("WijzigingsDatum") as "LaatsteWijziging"
        from "ProjectVersie"
        where "StatusId" = 3
    """
    session = SessionLocal()
    result = session.execute(text(query)).fetchone()
    session.close()
    if result is not None:
        return result[0]  # type: ignore
    else:
        return None
