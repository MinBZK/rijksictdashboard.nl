from pydantic import BaseModel


class Kengetallen(BaseModel):
    kengetallen: dict
    activiteiten: list[dict]
    ministeries: list[str]
