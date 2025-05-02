from fastapi import APIRouter

import app.schemas as schemas
from app.controllers.kwiv import get_kwiv_data
from app.types.misc import KwivJaar
from app.util.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/", response_model=schemas.KWIVData)
async def kwiv(
    jaar: KwivJaar, ministerie: str | None = None, category: str | None = None
):
    return await get_kwiv_data(ministerie=ministerie, jaar=jaar, category=category)
