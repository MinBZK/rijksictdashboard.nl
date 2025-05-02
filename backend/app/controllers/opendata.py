import io
from typing import TypedDict

import pandas as pd
from sqlalchemy.orm import Session

import app.models as models
import app.schemas as schemas
import app.util.exceptions as exceptions
from app.services import ProjectGetter
from app.util.dfs_to_excel import dict_to_spreadsheet


class ProjectExcelFileResponse(TypedDict):
    project_naam: str
    excel_file: io.BytesIO


def get_project_as_flat_excel_file(
    project_id: str, session: Session
) -> ProjectExcelFileResponse:
    model = models.project.ProjectViewIndicator
    query = (
        session.query(model)
        .filter(model.ProjectId == project_id, model.ProjectVersieStatusId == 3)
        .order_by(model.IndicatorLijstMeervoudsNaam, model.FormulierId)
    )
    projecten: list[models.project.ProjectViewIndicator] = query.all()
    data = [
        schemas.project.ProjectViewIndicator.model_validate(r).model_dump()
        for r in projecten
    ]
    df = pd.DataFrame(data)
    df["RijNummer"] = df.groupby(
        ["Naam", "IndicatorLijstMeervoudsNaam", "IndicatorTitel"]
    )["FormulierId"].rank(method="dense")
    available_columns = [
        col
        for col in [
            "Naam",
            "IndicatorLijstMeervoudsNaam",
            "RijNummer",
            "IndicatorTitel",
            "Waarde",
        ]
        if col in df.columns
    ]
    df = pd.DataFrame(df[available_columns])

    df.columns = df.columns.str.replace("IndicatorLijstMeervoudsNaam", "LijstNaam")
    df.columns = df.columns.str.replace("IndicatorTitel", "Attribuut")
    project_naam = (
        df["Naam"].iloc[0].replace(" ", "_") if "Naam" in df.columns else "project"
    )

    stream = io.BytesIO()
    df.to_excel(stream, index=False, engine="openpyxl")  # type: ignore

    return {"excel_file": stream, "project_naam": project_naam}


def get_project_as_nested_excel_file(project_id: str) -> ProjectExcelFileResponse:
    projecten = ProjectGetter(project_id=project_id).projecten

    if len(projecten) == 1:
        project = projecten[0]
        indicatorlijsten_dict = project.calculated_attributes.indicatorlijsten_as_dict
        excel_stream = dict_to_spreadsheet(
            data_dict=indicatorlijsten_dict, file_type="excel"
        )
        return {"excel_file": excel_stream, "project_naam": project.Naam}
    elif len(projecten) == 0:
        raise exceptions.ProjectNotFound(project_id)
    else:
        raise exceptions.MoreThanOneResult(project_id)
