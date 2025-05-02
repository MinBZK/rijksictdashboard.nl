from pydantic import BaseModel


class HealthStatus(BaseModel):
    name: str
    health_status: bool
    description: str
