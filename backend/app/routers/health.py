from dataclasses import dataclass
from functools import partial
from typing import Callable

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

import app.controllers as controllers
import app.models as models
import app.schemas as schemas
from app.middleware import get_db
from app.schemas.health import HealthStatus
from app.util.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


def check_health(func) -> bool:
    healthy = False
    try:
        func()
        healthy = True
    finally:
        return healthy


@dataclass
class HealthCheck:
    func: Callable
    name: str
    description_ok: str
    description_nok: str

    def check(self):
        return check_health(self.func)

    @property
    def status(self) -> HealthStatus:
        health_status = check_health(self.func)
        return HealthStatus(
            **{
                "name": self.name,
                "health_status": health_status,
                "description": (
                    self.description_ok if health_status else self.description_nok
                ),
            }
        )


def get_projecten(db: Session):
    return controllers.Project(session=db, filters=[]).get_many(
        limit=1, return_projects=True, sorting=[]
    )


def get_first_project(db: Session) -> models.ProjectView:
    # Get proejct
    project = db.scalars(select(models.ProjectView)).first()

    if project is None:
        raise ValueError("No project found")
    return project


@router.get("/", response_model=list[schemas.HealthStatus])
def healthcheck(db: Session = Depends(get_db)):
    health_checks = [
        HealthCheck(
            name="project",
            description_ok="Projecten retrieved successfully",
            description_nok="Unable to retrieve projecten",
            func=partial(get_projecten, db),
        ),
        HealthCheck(
            name="database",
            description_ok="Project view gave a result",
            description_nok="Project view did not return any results",
            func=partial(get_first_project, db),
        ),
    ]

    health_statuses = [h.status for h in health_checks]

    status_code = (
        status.HTTP_500_INTERNAL_SERVER_ERROR
        if any([s.health_status is False for s in health_statuses])
        else status.HTTP_200_OK
    )

    return JSONResponse(
        status_code=status_code, content=[h.model_dump() for h in health_statuses]
    )
