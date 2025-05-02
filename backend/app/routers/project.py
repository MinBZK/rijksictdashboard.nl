from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

import app.controllers as controllers
import app.models as models
import app.schemas as schemas
from app.middleware import get_db
from app.routers.dependencies import (
    parse_attributes,
    parse_stringified_filters,
    parse_stringified_sorting,
)
from app.types import ProjectAttributeSorting, ProjectFilter
from app.types.jbr_activiteiten_overzicht import ActiviteitMetrics
from app.util.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/", response_model=schemas.project.ProjectenMetMetrics)
async def get_many(
    limit: int | None = None,
    db: Session = Depends(get_db),
    page: int = 1,
    search: str | None = None,
    filters: list[ProjectFilter] = Depends(parse_stringified_filters),
    sorting: list[ProjectAttributeSorting] = Depends(parse_stringified_sorting),
    aggregation_attributes: list[ActiviteitMetrics] = Depends(parse_attributes),
    get_projects: bool = True,
):
    projecten = controllers.Project(
        session=db,
        search=search,
        filters=filters,
    ).get_many(
        limit=limit,
        aggregation_attributes=aggregation_attributes,
        page=page,
        sorting=sorting,
        return_projects=get_projects,
    )

    return projecten


def preview_project_is_authorized(
    request_token: str | None, db: Session, project_versie_id: int | None
) -> bool:
    preview_token = db.scalars(
        select(models.ProjectVersiePreviewToken).where(
            models.ProjectVersiePreviewToken.ProjectVersieId == project_versie_id,
            models.ProjectVersiePreviewToken.Token == request_token,
        )
    ).first()

    if request_token is None or preview_token is None:
        return False
    else:
        return controllers.validate_project_token(
            request_token=request_token,
            project_versie_token=preview_token.Token,
            project_versie_token_aanmaakdatum=preview_token.AanmaakDatum,
        )


def get_project_id(project_id: str):
    try:
        return UUID(project_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{project_id} is not a valid UUID",
        )


def get_legacy_project_id(unparsed_project_id: str, db: Session):
    project = db.scalars(
        select(models.ProjectViewMetWaardes).where(
            models.ProjectViewMetWaardes.LegacyProjectId == int(unparsed_project_id)
        )
    ).first()
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Geen activiteit gevonden met legacy id {unparsed_project_id}.",
        )
    return UUID(project.ProjectId)


def handle_get_project(
    project_id: UUID, project_versie_id: int | None, token: str | None, db: Session
):
    model = models.project.ProjectViewMetWaardes
    stmt = select(model).where(model.ProjectId == project_id).order_by(model.Naam)

    is_default_request = project_versie_id is None and token is None
    is_preview_request = project_versie_id is not None and token is not None

    if not is_default_request and not is_preview_request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project versie id en token zijn beide benodigd.",
        )
    else:
        project_authorized = is_default_request or (
            is_preview_request
            and preview_project_is_authorized(
                request_token=token, db=db, project_versie_id=project_versie_id
            )
        )

        if not project_authorized:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Ongeldig token",
            )

        project_query = (
            stmt.where(model.ProjectVersieStatusId == 3)
            if is_default_request
            else stmt.where(model.ProjectVersieId == project_versie_id)
        )

        project = db.scalars(project_query).first()
        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Geen activiteit gevonden.",
            )
        else:
            project.set_calculated_attributes(year=None)
            return project.merged_attributes


@router.get(
    "/{unparsed_project_id}",
    response_model=schemas.project.ProjectMetAlleMetricsEnIndicatorLijsten,
)
async def get_one(
    unparsed_project_id: str,
    is_legacy_id: bool = Query(False),
    project_versie_id: int | None = None,
    token: str | None = None,
    db: Session = Depends(get_db),
):
    project_id = (
        get_legacy_project_id(unparsed_project_id, db)
        if is_legacy_id
        else get_project_id(unparsed_project_id)
    )
    return handle_get_project(
        project_id=project_id, project_versie_id=project_versie_id, token=token, db=db
    )


@router.get("/laatst-gewijzigd/{aantal}", response_model=list[schemas.project.Project])
async def laatst_gewijzigd(aantal: int, db: Session = Depends(get_db)):
    model = models.project.ProjectView

    projecten = (
        db.query(model)
        .order_by(model.ProjectVersieWijzigingsDatum.desc())
        .all()[:aantal]
    )

    return projecten
