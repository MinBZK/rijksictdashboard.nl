import httpx
from fastapi import APIRouter
from pydantic import BaseModel

from app.config.env import settings
from app.util.logger import get_logger

router = APIRouter()

logger = get_logger(__name__)


class ScraperSearchResponse(BaseModel):
    url: str
    title: str
    score: int


def get_search_results(search_query: str):
    enable_scraper_search = settings.ENABLE_SCRAPER_SEARCH == "1"
    if not enable_scraper_search:
        logger.info("Scraper search is disabled.")
        return []

    with httpx.Client() as client:
        url = f"{settings.SCRAPER_SERVER}/domain/{settings.SCRAPER_DOMAIN}/search/{search_query}"
        try:
            response = client.get(
                url,
                params={"base_title": settings.APPLICATION_TITLE, "title_only": True},
            )

            if response.status_code != 200:
                logger.error(f"Scraper: {response.status_code}, {url}, {response.text}")
                return []

            logger.info(f"Requested URL: {url}")
            results = response.json()
            return [ScraperSearchResponse(**result) for result in results]
        except httpx.ConnectError as e:
            logger.error(f"Connection failed with url {url}")
            logger.error(f"Scraper: {e}")
            return []
