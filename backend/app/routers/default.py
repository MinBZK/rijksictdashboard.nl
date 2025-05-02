from fastapi import APIRouter

from app.config.env import settings
from app.util.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/")
async def root():
    return {"message": "Hello World", "namespace": settings.DEPLOYMENT_ENV}
