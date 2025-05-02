from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

import app.controllers as controllers
import app.schemas as schemas
from app.middleware import get_db
from app.util.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/{search_query}", response_model=schemas.SearchResults)
async def search(
    search_query: str, category: str = Query(None), session: Session = Depends(get_db)
):
    return await controllers.Project(
        session=session,
        filters=[],
        search=search_query,
    ).get_search_results(category)
