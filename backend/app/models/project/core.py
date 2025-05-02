import datetime
from logging import getLogger

from sqlalchemy import (
    ARRAY,
    TIMESTAMP,
    UUID,
    Boolean,
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

import app.schemas as schemas
from app.config.indicatorlijst import indicatorlijst_config
from app.models.misc import Base
from app.models.project.calculated_models.indicatorlijst import (
    Formulier,
    Indicatorlijst,
)
from app.schemas.project import IndicatorLijst

from .calculated_models import ProjectCalculated

logger = getLogger("uvicorn")


class ProjectView(Base):
    """
    A model for the project view. The view is defined in v_project_agg.sql and is updated on each application startup.
    """

    __tablename__ = "vProjectAgg"

    ProjectId: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True)
    LegacyProjectId: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Slug: Mapped[str] = mapped_column(String)
    Naam: Mapped[str] = mapped_column(String)
    LaatsteVersieId: Mapped[int] = mapped_column(Integer)
    ProjectVersieId: Mapped[int] = mapped_column(Integer)
    ProjectVersie: Mapped[int] = mapped_column(Integer)
    ProjectVersieStatusId: Mapped[int] = mapped_column(Integer)
    ProjectVersieStatusNaam: Mapped[str] = mapped_column(String)
    Samenvatting: Mapped[dict] = mapped_column(JSONB)
    IndicatorLijstBeschikbaar: Mapped[list[str]] = mapped_column(ARRAY(String))
    MinisterieId: Mapped[int] = mapped_column(Integer, ForeignKey("Ministerie.Id"))
    MinisterieAfkorting: Mapped[str] = mapped_column(String)
    Onderwerp: Mapped[str] = mapped_column(String)
    ProjectVersieWijzigingsDatum: Mapped[datetime.date] = mapped_column(Date)
    MinisterieNaam: Mapped[str] = mapped_column(String)
    ProjectStatus: Mapped[str] = mapped_column(String)
    StartDatum: Mapped[str | None] = mapped_column(String)
    PeilDatum: Mapped[datetime.datetime] = mapped_column(Date)
    PeilDatumJaar: Mapped[int] = mapped_column(Integer)
    OrganisatieNaam: Mapped[str] = mapped_column(String)


class ProjectViewMetWaardes(ProjectView):
    IndicatorLijstWaardes: Mapped[list[dict]] = mapped_column(JSONB)

    @property
    def IndicatorLijstWaardesGecorrigeerd(self) -> list[dict]:
        indicatorlijsten = [
            IndicatorLijst.model_validate(il) for il in self.IndicatorLijstWaardes
        ]

        for il in indicatorlijsten:
            il_caclulated = Indicatorlijst(
                parsed_indicatorlijst=il,
                naam=il.IndicatorLijstMeervoudsNaam,
                project_naam=self.Naam,
            )
            il.FormulierDict = il_caclulated.formulieren_as_dict
            il_config = indicatorlijst_config.get(il.IndicatorLijstMeervoudsNaam)
            date_index_column = (
                il_config["date_index_column"] if il_config is not None else None
            )
            data_types = il_config["data_types"] if il_config is not None else {}
            for f in il.Formulier:
                indicatortitels = [w.IndicatorTitel for w in f.FormulierWaardes]
                calculated_formulier = Formulier(
                    parsed_formulier_waardes=f.FormulierWaardes,
                    date_index_column=date_index_column,
                    data_types=data_types,
                    indicatortitels=indicatortitels,
                    indicatorlijstnaam=il.IndicatorLijstMeervoudsNaam,
                )
                f.Dict = calculated_formulier.as_dict
                f.FormulierWaardes = calculated_formulier.parsed_formulier_waardes

        return [il.model_dump() for il in indicatorlijsten]

    @property
    def calculated_attributes(self) -> ProjectCalculated:
        if self._calculated_attributes is not None:
            return self._calculated_attributes
        else:
            raise RuntimeError(
                "Calculated attributes are not set yet, call the setter first."
            )

    def set_calculated_attributes(self, year: int | None):
        self._calculated_attributes = self.get_calculated_attributes(year=year)
        self._set_merged_attributes()

    def get_calculated_attributes(self, year: int | None = None):
        start_datum_dt = (
            datetime.datetime.strptime(self.StartDatum, "%Y-%m-%d")
            if self.StartDatum
            else None
        )
        return ProjectCalculated(
            naam=self.Naam,
            project_id=self.ProjectId,
            ministerie_afkorting=self.MinisterieAfkorting,
            onderwerp=self.Onderwerp,
            startdatum=start_datum_dt,
            projectstatus=self.ProjectStatus,
            indicatorlijst_waardes=[
                schemas.IndicatorLijst(**il) for il in self.IndicatorLijstWaardes
            ],
            ministerie_naam=self.MinisterieNaam,
            jbr_jaar=year,
            organisatie_naam=self.OrganisatieNaam,
        )

    @property
    def merged_attributes(self) -> schemas.ProjectMetAlleMetricsEnIndicatorLijsten:
        return self._merged_attributes

    def _set_merged_attributes(self):
        dict_db = schemas.ProjectMetIndicatorlijsten.model_validate(self).model_dump()
        dict_calculated = self.calculated_attributes.project_summary_jbr.model_dump()
        dict_merged = {**dict_db, **dict_calculated}
        self._merged_attributes = schemas.ProjectMetAlleMetricsEnIndicatorLijsten(
            **dict_merged
        )


class ProjectViewIndicator(Base):
    __tablename__ = "vProjectIndicator"

    Naam = Column(Text)
    AntwoordId = Column(Integer, primary_key=True)
    ProjectVersieId = Column(Integer)
    IndicatorId = Column(Integer)
    IndicatorLijstId = Column(String)
    ProjectId = Column(String)
    FormulierId = Column(String)
    ProjectVersie = Column(Integer)
    ProjectVersieStatusId = Column(Integer)
    ProjectVersieStatusNaam = Column(String)
    IndicatorLijstMeervoudsNaam = Column(Text)
    IndicatorLijstEnkelFormulier = Column(Boolean)
    FormulierAanmaakDatum = Column(TIMESTAMP)
    WijzigingsDatum = Column(Date)
    IndicatorTitel = Column(Text)
    Waarde = Column(Text)
    MinisterieNaam = Column(Text)


class ProjectVersiePreviewToken(Base):
    __tablename__ = "ProjectVersiePreviewToken"

    Id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ProjectVersieId: Mapped[int] = mapped_column(Integer)
    Token: Mapped[str] = mapped_column(String)
    AanmaakDatum: Mapped[datetime.datetime] = mapped_column(Date)
