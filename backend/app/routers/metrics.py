from fastapi import APIRouter

from app.controllers import ProjectCollection
from app.util.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/activiteit/{year}")
def get_activiteiten(year: int | None = None):
    return ProjectCollection(year=year).get_projecten_met_toelichting()
