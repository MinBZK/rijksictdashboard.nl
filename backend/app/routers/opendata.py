from datetime import date
from enum import Enum

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.controllers as controllers
from app.controllers import ProjectCollection
from app.controllers.opendata import (
    get_project_as_flat_excel_file,
    get_project_as_nested_excel_file,
)
from app.middleware import get_db
from app.types.misc import SpreadsheetType
from app.util import exceptions
from app.util.clean import clean_text
from app.util.dfs_to_excel import ExcelSheet, dict_to_spreadsheet, excel_to_ods
from app.util.logger import get_logger
from app.util.response import get_file_stream_response

from .dependencies.excel_config import (
    column_order,
    excel_column_mapping,
    get_excel_toelichting_cells,
)

router = APIRouter()
logger = get_logger(__name__)


@router.get("/json")
async def project_compact(db: Session = Depends(get_db)):
    return controllers.Project(
        session=db,
        with_attributes=True,
        filters=[],
    ).get_many_compact()


class ExportFormat(str, Enum):
    FLAT = "flat"
    NESTED = "nested"


@router.get(
    "/spreadsheet/{spreadsheet_type}/{project_id}",
    response_description="xlsx",
)
async def get_activiteit(
    project_id: str,
    spreadsheet_type: SpreadsheetType = "excel",
    export_format: ExportFormat = ExportFormat.NESTED,
    db: Session = Depends(get_db),
):
    try:
        if export_format == ExportFormat.FLAT:
            excel_response = get_project_as_flat_excel_file(
                project_id=project_id, session=db
            )
        else:
            excel_response = get_project_as_nested_excel_file(project_id=project_id)

        filename = clean_text(excel_response["project_naam"])
        if spreadsheet_type == "excel":
            return get_file_stream_response(
                stream=excel_response["excel_file"],
                filename=f"{filename}.xlsx",
            )
        else:
            return get_file_stream_response(
                stream=excel_to_ods(excel_response["excel_file"]),
                filename=f"{filename}.ods",
            )
    except exceptions.ProjectNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Geen projecten gevonden voor {str(e)}",
        )
    except exceptions.MoreThanOneResult as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Meer dan één projecten gevonden voor {str(e)}",
        )


@router.get("/spreadsheet/{spreadsheet_type}")
def get_alle_activiteiten(
    spreadsheet_type: SpreadsheetType = "excel",
    year: int | None = None,
):
    metrics = ProjectCollection(year=year)
    metric_df: pd.DataFrame = metrics.activiteit_overzicht
    metric_df.drop("ActiviteitId", axis=1, inplace=True)

    valid_columns = [col for col in column_order if col in metric_df.columns]
    if len(valid_columns) < len(column_order):
        missing_columns = set(column_order) - set(valid_columns)
        raise ValueError(
            f"The following columns are missing from the DataFrame: {', '.join(missing_columns)}"
        )
    metric_df = metric_df.loc[:, valid_columns]
    metric_df.rename(
        columns=excel_column_mapping,
        inplace=True,
    )

    matrix = {"Activiteitenoverzicht": metric_df.to_dict(orient="records")}

    excel_stream = dict_to_spreadsheet(
        data_dict=matrix,
        file_type=spreadsheet_type,
        sheet_names={"Algemeen": "Activiteitenoverzicht"},
        default_sheet=ExcelSheet(
            title="Toelichting", cells=get_excel_toelichting_cells()
        ),
    )

    extension = ".xlsx" if spreadsheet_type == "excel" else ".ods"
    filename = (
        "rijksictdashboard_activiteitenoverzicht_" + str(date.today()) + extension
    )
    return get_file_stream_response(excel_stream, filename=filename)
