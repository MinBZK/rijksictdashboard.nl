from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.controllers import ProjectCollection
from app.util.dfs_to_excel import dict_to_spreadsheet
from app.util.logger import get_logger
from app.util.response import get_file_stream_response

router = APIRouter()
logger = get_logger(__name__)


@router.get("/{year}")
def get_rapportage(year: int):
    metrics = ProjectCollection(year=year)
    filename = f"jbr_rapportage_{year}.xlsx"

    sheet_names = {
        "algemeen": "Algemeen",
        "Aantal ICT projecten per status": "AantalActiviteitenPerStatus",
        "Verschil initiele en actuele doorlooptijd (aantallen)": "VerschilDoorlooptijdAantal",
        "Verschil initiele en actuele doorlooptijd (%)": "VerschilDoorlooptijdPercentage",
        "Geschatte kosten (aantallen)": "GeschatteKosten",
        "Redenen voor herijkingen": "Herijkingen",
        "Daadwerkelijke uitgaven per categorie": "UitgavenPerCategorie",
        "Meerjarige kosten": "MeerjarigeKosten",
        "Ontwikkelpartijen": "Ontwikkelpartijen",
    }

    rapportage_and_matrix = {
        "ActiviteitenMatrix": metrics.activiteit_overzicht.to_dict(orient="records"),
        **metrics.kengetallen,
    }

    excel_file = dict_to_spreadsheet(
        data_dict=rapportage_and_matrix, file_type="excel", sheet_names=sheet_names
    )

    return get_file_stream_response(stream=excel_file, filename=filename)


@router.get("/{year}/activiteit/{activiteit_id}")
def get_activiteit(year: int, activiteit_id: str):
    jbr = ProjectCollection(year=year, activiteit_id=activiteit_id)
    project = jbr.get_project_by_id(activiteit_id=activiteit_id)
    if project is not None:
        toelichting = project.calculated_attributes.toelichting
        filename = f"jbr_rapportage_{project.Naam}_{year}.xlsx"
        return get_file_stream_response(
            stream=dict_to_spreadsheet(
                data_dict=toelichting,
                file_type="excel",
            ),
            filename=filename,
        )
    else:
        raise HTTPException(status_code=404, detail="Geen activiteit gevonden")


@router.get("/activiteiten/{year}")
def get_activiteiten_csv(year: int):
    file_name = "JBR-" + str(year) + "-RijksICTDashboard.csv"
    file_path = f"app/assets/{file_name}"

    return FileResponse(file_path, filename=file_name, media_type="text/csv")
