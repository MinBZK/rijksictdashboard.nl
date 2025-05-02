from pydantic import BaseModel, ConfigDict


class Ministerie(BaseModel):
    Naam: str
    Afkorting: str

    model_config = ConfigDict(from_attributes=True)
