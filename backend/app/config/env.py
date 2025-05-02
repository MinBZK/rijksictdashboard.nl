from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PreditorStatus = Literal["draft", "published", "dummy"]


class Settings(BaseSettings):
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "rid-data"
    DEPLOYMENT_ENV: Literal["local", "acc", "tst", "prd"] = "local"
    DISABLE_WACHTER_INITIALIZATION: Literal["0", "1"] = "0"
    SHOW_API_DOCS: Literal["0", "1"] = "0"
    PREDITOR_SECRET_KEY: str = Field(default="", min_length=0)
    PREDITOR_TOTP_SEED: str = Field(default="", min_length=0)
    PREDITOR_STATUS: PreditorStatus = Field(default="published")
    ENABLE_SCRAPER_SEARCH: Literal["0", "1"] = "0"
    SCRAPER_SERVER: str = Field(default="", min_length=1)
    APPLICATION_TITLE: str = "Rijks ICT-dashboard"
    SCRAPER_DOMAIN: str = Field(default="localhost:5173", min_length=1)
    PVC_DIRECTORY: str = Field(default="./app/data/pvc/", min_length=2)

    model_config = SettingsConfigDict(extra="allow", env_file=".env")


settings = Settings()
