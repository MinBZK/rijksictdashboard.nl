from fastapi import HTTPException

from app.models import Ministerie

from .get_db import get_db


def validate_ministerie_naam(ministerie: str | None = None):
    if ministerie is not None:
        session = next(get_db())
        result = (
            session.query(Ministerie).filter(Ministerie.Naam.in_([ministerie])).all()
        )
        if len(result) == 0:
            raise HTTPException(
                status_code=400,
                detail=f"{ministerie} is geen geldige ministerienaam.",
            )
    return ministerie
