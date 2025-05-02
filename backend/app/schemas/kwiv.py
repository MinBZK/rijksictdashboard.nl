from pydantic import BaseModel


class ChartdataPoint(BaseModel):
    x: str
    y: float
    y: float
    label: str


class KWIVData(BaseModel):
    datapoints: list[ChartdataPoint]
    available_ministeries: list[str]
    available_categories: list[str]
