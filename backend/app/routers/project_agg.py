from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.controllers as controllers
import app.schemas as schemas
from app.middleware import get_db
from app.routers.dependencies import parse_stringified_filters
from app.types import ProjectFilter
from app.util.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


def validate_attribute(attribute: str):
    valid_attributes = schemas.ProjectSamenvattingJBR.model_fields.keys()
    if attribute in valid_attributes:
        return attribute
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{attribute} is not a valid attribute",
        )


@router.get("/agg/{attribute}")
async def agg_per_attribute(
    attribute: str = Depends(validate_attribute),
    filters: list[ProjectFilter] = Depends(parse_stringified_filters),
    db: Session = Depends(get_db),
):
    return controllers.Project(
        session=db,
        filters=filters,
    ).count_values(attribute=attribute)
