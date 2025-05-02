from fastapi import APIRouter

import app.controllers.ministerie as controller
from app.schemas import Ministerie
from app.util.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/", response_model=list[Ministerie])
async def get_all():
    return controller.get_many()
