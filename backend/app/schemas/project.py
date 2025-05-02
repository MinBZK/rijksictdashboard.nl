from __future__ import annotations

import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.config.indicatorlijst import IndicatorlijstConfig, indicatorlijst_config
from app.types import IndicatorlijstNamen

from .jbr import (
    ProjectSamenvattingAttributen,
    ProjectSamenvattingCore,
    ProjectSamenvattingJBR,
)


class FormulierWaarde(BaseModel):
    IndicatorTitel: str
    IndicatorIndex: int
    IndicatorAntwoordTypeNaam: str
    Waarde: str | None


class Formulier(BaseModel):
    FormulierId: str
    FormulierAanmaakDatum: datetime.datetime
    FormulierWaardes: list[FormulierWaarde]
    Dict: dict | None = None


class IndicatorLijst(BaseModel):
    IndicatorLijstId: str
    IndicatorLijstMeervoudsNaam: IndicatorlijstNamen
    IndicatorLijstEnkelFormulier: bool
    IndicatorLijstIndex: int
    Formulier: list[Formulier]
    FormulierDict: list[dict] | None = None

    # Calculated fields
    DatumIndexVeld: str | None

    def __init__(self, **data):
        """
        Add calculated fields
        """
        indicatorlijst_naam = data.get("IndicatorLijstMeervoudsNaam")

        # find datum_index_veld in config
        datum_index_veld = None
        if indicatorlijst_naam is not None:
            indicatorlijst_config = self.__get_config(
                indicatorlijst_naam=indicatorlijst_naam
            )
            if indicatorlijst_config is not None:
                datum_index_veld = indicatorlijst_config["date_index_column"]

        # If the object already contains a datum index veld, because it has already been
        # converted to a Pydantic model, exclude it from the **data kwargs to prevent an error.
        excluded_data_keys = ["DatumIndexVeld"]
        data_without_excluded_keys = {
            k: v for k, v in data.items() if k not in excluded_data_keys
        }

        super().__init__(DatumIndexVeld=datum_index_veld, **data_without_excluded_keys)

    def __get_config(self, indicatorlijst_naam: str) -> IndicatorlijstConfig | None:
        """
        Returns config for indicatorlijst.
        """
        indicatorlijst_naam_enum: IndicatorlijstNamen | None = next(
            (naam for naam in IndicatorlijstNamen if naam.value == indicatorlijst_naam),
            None,
        )

        if indicatorlijst_naam_enum is not None:
            config = indicatorlijst_config.get(indicatorlijst_naam_enum)
            if config is not None:
                return config


class Project(BaseModel):
    ProjectId: str
    Naam: str
    Slug: str
    ProjectVersieId: int
    ProjectVersie: int
    LegacyProjectId: int | None
    # Samenvatting: dict | None
    MinisterieNaam: str
    MinisterieAfkorting: str
    ProjectVersieWijzigingsDatum: datetime.datetime
    ProjectVersieStatusNaam: str
    Onderwerp: str | None
    ProjectVersieStatusId: int
    ProjectStatus: str | None
    StartDatum: datetime.date | None
    PeilDatum: datetime.date | None
    OrganisatieNaam: str | None

    model_config = ConfigDict(from_attributes=True)


class ProjectAttributenBerekend(BaseModel):
    in_uitvoering_in_jbr_jaar: bool
    project_summary_jbr: ProjectSamenvattingJBR
    toelichting_herijkingen: list[dict]
    toelichting_mijlpalen: list[dict]
    toelichting_ontwikkelpartijen: list[dict]
    toelichting_baten: list[dict]
    bit_adviezen: list[dict]
    indicatorlijsten_as_dict: dict
    toelichting: dict

    model_config = ConfigDict(from_attributes=True)


class ProjectMetIndicatorlijsten(Project):
    # IndicatorLijstWaardes: list[IndicatorLijst] = Field(exclude=True)
    IndicatorLijstWaardesGecorrigeerd: list[IndicatorLijst]


class ProjectMetBerekendeAttributen(ProjectMetIndicatorlijsten):
    calculated_attributes: ProjectAttributenBerekend


class Aggregation(BaseModel):
    attribute: str
    count: int

    model_config = ConfigDict(from_attributes=True)


class Aggregation2(BaseModel):
    attribute: str
    count: int


class ProjectViewIndicator(BaseModel):
    Naam: str
    ProjectVersieStatusId: int
    IndicatorLijstMeervoudsNaam: str
    FormulierId: UUID
    IndicatorTitel: str
    Waarde: str | None
    WijzigingsDatum: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class AttributeAggregation(BaseModel):
    aggregation_column: str
    aggregation_value: str
    count: int

    model_config = ConfigDict(from_attributes=True)


class ProjectAttributeAggregation(BaseModel):
    aggregation_attribute: str
    values: list[AttributeAggregation]


class ProjectMetCoreMetrics(ProjectSamenvattingCore, Project):
    pass


class ProjectMetAlleMetrics(ProjectMetCoreMetrics, ProjectSamenvattingAttributen):
    pass


class ProjectMetAlleMetricsEnIndicatorLijsten(
    ProjectMetAlleMetrics, ProjectMetIndicatorlijsten
):
    pass


class Metrics(BaseModel):
    kengetallen: dict
    ministeries: list[str]
    projecten: dict[str, list[Project]]

    model_config = ConfigDict(from_attributes=True)


class ProjectenMetMetrics(BaseModel):
    metrics: Metrics
    results: list[ProjectMetCoreMetrics]
    total_count: int
    aggregations: list[ProjectAttributeAggregation]
    ministeries: list[str]
