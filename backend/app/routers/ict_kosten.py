from fastapi import APIRouter

from app.controllers.ict_kosten import get_ict_kosten
from app.util.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/")
async def kostenstelsels(
    ministerie: str | None = None,
):
    return get_ict_kosten(ministerie=ministerie)
