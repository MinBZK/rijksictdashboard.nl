import datetime
from dataclasses import dataclass
from enum import Enum
from typing import Any, Literal

import pandas as pd
import pytz
from dateutil.relativedelta import relativedelta

from app.schemas import IndicatorLijst, ProjectSamenvattingJBR
from app.types import (
    ActiviteitMetrics,
    DataTypes,
    DoorlooptijdEnKosten,
    IndicatorlijstFilter,
    IndicatorlijstNamen,
    Kwaliteitstoetsen,
    Mijlpalen,
    Ontwikkelpartijen,
    TweedeKamerstukken,
)
from app.util.logger import get_logger
from app.util.misc import get_timedelta_in_years

from .common import DEFAULT_DATE
from .formulier import Formulier
from .indicatorlijst import Indicatorlijst

logger = get_logger(__name__)


@dataclass
class Project:
    indicatorlijst_waardes: list[IndicatorLijst]
    naam: str
    project_id: str
    ministerie_afkorting: str
    organisatie_naam: str
    onderwerp: str
    ministerie_naam: str
    startdatum: datetime.datetime | None
    projectstatus: str
    jbr_jaar: int | None

    def __post_init__(self):
        self.indicatorlijsten: list[Indicatorlijst] = []

        self.__doorlooptijd_kosten_meest_recent = (
            self.__get_doorlooptijd_kosten_meest_recent(year=self.jbr_jaar)
        )
        self.acict_adviezen = self.__get_acict_adviezen()
        self.toelichting_herijkingen = self.__get_toelichting_herijkingen()
        self.toelichting_baten = self.__get_toelichting_baten()
        self.toelichting_mijlpalen = self.__get_toelichting_mijlpalen()
        self.toelichting_ontwikkelpartijen = self.__get_toelichting_ontwikkelpartijen()

        self.__doorlooptijd_kosten_initieel = self.__get_doorlooptijd_kosten_initieel()
        self.__actueel_geschatte_einddatum = self.__get_actueel_geschatte_einddatum()
        self.project_summary_jbr = self.__get_project_summary_jbr()

    @property
    def indicatorlijsten_as_dict(
        self,
    ) -> dict[str, list[dict[str, Any]] | dict[str, Any] | None]:
        beschikbare_indicatorlijsten = sorted(
            [il.IndicatorLijstMeervoudsNaam for il in self.indicatorlijst_waardes]
        )

        amsterdam_tz = pytz.timezone("Europe/Amsterdam")
        current_time_amsterdam = datetime.datetime.now(amsterdam_tz).strftime(
            "%d-%m-%Y %H:%M:%S"
        )

        il_dict: dict[str, list[dict[str, Any]] | dict[str, Any] | None] = {
            "ProjectInformatie": {
                "Naam": self.naam,
                "Ministerie": self.ministerie_naam,
                "Organisatie": self.organisatie_naam,
                "Id": self.project_id,
                "Url": f"https://rijksictdashboard.nl/ict-activiteiten/{self.project_id}",
                "Geëxporteerd op (tijdzone Amsterdam)": current_time_amsterdam,
            }
        }

        for il_naam in beschikbare_indicatorlijsten:
            lijst = self.__get_indicatorlijst(il_naam)
            lijst_dict = lijst.formulieren_as_dict if lijst else None

            # Indien indicatorlijst 'enkel' is, wijs dan alleen de eerste rij toe, dit is handig voor weergave in Excel.
            il_dict[il_naam.value] = (
                lijst_dict[0]
                if lijst_dict is not None
                and lijst is not None
                and lijst.parsed_indicatorlijst.IndicatorLijstEnkelFormulier
                else lijst_dict
            )

        return il_dict

    @property
    def indicatorlijst_algemeen_dict(self):
        indicatorlijst_algemeen = self.__get_indicatorlijst(
            indicatorlijst_naam=IndicatorlijstNamen.ALGEMEEN
        )
        assert indicatorlijst_algemeen
        return indicatorlijst_algemeen.formulieren_as_dict[0]

    def __get_indicatorlijst(
        self,
        indicatorlijst_naam: IndicatorlijstNamen,
    ) -> Indicatorlijst | None:
        # Check if indicatorlijst object has already been created
        matched_indicatorlijsten = [
            il for il in self.indicatorlijsten if il.naam == indicatorlijst_naam
        ]

        if len(matched_indicatorlijsten) == 1:
            il = matched_indicatorlijsten[0]
            return il
        else:
            # generate indicatorlijst object if it has not yet been created
            matched_results = [
                il
                for il in self.indicatorlijst_waardes
                if il.IndicatorLijstMeervoudsNaam == indicatorlijst_naam
            ]
            if len(matched_results) == 1:
                il = Indicatorlijst(
                    parsed_indicatorlijst=matched_results[0],
                    naam=indicatorlijst_naam,
                    project_naam=self.naam,
                )
                self.indicatorlijsten.append(il)
                return il
            else:
                return None

    def __find_formulier(
        self,
        indicatorlijst_naam: IndicatorlijstNamen,
        indicator_titel: str,
        indicator_waarde: str,
    ) -> dict | None:
        indicatorlijst = self.__get_indicatorlijst(
            indicatorlijst_naam=indicatorlijst_naam
        )

        if indicatorlijst is not None:
            formulieren = indicatorlijst.formulieren_as_dict

            formulier_initieel_matched = [
                f for f in formulieren if f.get(indicator_titel) == indicator_waarde
            ]
            if len(formulier_initieel_matched) == 1:
                return formulier_initieel_matched[0]
            elif len(formulier_initieel_matched) > 1:
                self.__log_error(
                    f"{indicatorlijst_naam.value}: meer dan één formulier gevonden voor {indicator_titel}={indicator_waarde}"  # noqa: E501
                )
                return formulier_initieel_matched[0]
            else:
                self.__log_error(
                    f"{indicatorlijst_naam.value}: geen formulier gevonden voor {indicator_titel}={indicator_waarde}"
                )

    def __log_error(self, message: str):
        # logger.error(f"Project {self.parsed_model.Naam} | {message}")
        pass

    def __get_actueel_geschatte_einddatum(self) -> datetime.date | None:
        return self.__doorlooptijd_kosten_meest_recent.get(
            DoorlooptijdEnKosten.ACTUEEL_GESCHATTE_EINDDATUM, None
        )

    @property
    def __initieel_geschatte_einddatum(self):
        doorlooptijd_kosten_initieel = self.__doorlooptijd_kosten_initieel
        return doorlooptijd_kosten_initieel.get(
            DoorlooptijdEnKosten.ACTUEEL_GESCHATTE_EINDDATUM, None
        )

    @property
    def in_uitvoering_in_jbr_jaar(self) -> bool:
        indicatorlijst_doorlooptijd_en_kosten = self.__get_indicatorlijst(
            indicatorlijst_naam=IndicatorlijstNamen.DOORLOOPTIJD_EN_KOSTEN
        )

        indicatorlijst_peildatum_en_status = self.__get_indicatorlijst(
            indicatorlijst_naam=IndicatorlijstNamen.PEILDATUM_EN_STATUS
        )

        peildatum_uit_peildatum_en_status_in_jbr_jaar = False
        peildatum_uit_doorlooptijd_en_kosten_in_jbr_jaar = False

        afgerond_in_of_na_jbr_jaar = (
            self.__actueel_geschatte_einddatum.year >= self.jbr_jaar
            if self.__actueel_geschatte_einddatum and self.jbr_jaar
            else False
        )

        eindjaar_bekend = self.__actueel_geschatte_einddatum is not None

        if indicatorlijst_peildatum_en_status is not None:
            df_peildatum_en_status = (
                indicatorlijst_peildatum_en_status.formulieren_as_df
            )
            if "Peildatum" in list(df_peildatum_en_status.columns):
                df_peildatum_en_status["peildatum_jaar"] = df_peildatum_en_status[
                    "Peildatum"
                ].dt.year
                peildatum_jaar = int(df_peildatum_en_status.iloc[0]["peildatum_jaar"])  # type: ignore
                peildatum_uit_peildatum_en_status_in_jbr_jaar = (
                    peildatum_jaar == self.jbr_jaar
                )

        if (
            indicatorlijst_doorlooptijd_en_kosten is not None
            and indicatorlijst_doorlooptijd_en_kosten.date_index_column is not None
            and indicatorlijst_doorlooptijd_en_kosten.has_valid_date_index_column
            and self.jbr_jaar
        ):
            df = indicatorlijst_doorlooptijd_en_kosten.formulieren_as_df

            df_kosten_in_jbr_jaar = df[
                df[indicatorlijst_doorlooptijd_en_kosten.date_index_column].dt.year
                >= self.jbr_jaar
            ]
            peildatum_uit_doorlooptijd_en_kosten_in_jbr_jaar = (
                len(df_kosten_in_jbr_jaar.index) > 0
            )

        return (
            peildatum_uit_doorlooptijd_en_kosten_in_jbr_jaar
            or peildatum_uit_peildatum_en_status_in_jbr_jaar
        ) and (afgerond_in_of_na_jbr_jaar or not eindjaar_bekend)

    def __get_doorlooptijd_kosten_meest_recent(self, year: int | None) -> dict:
        indicatorlijst = self.__get_indicatorlijst(
            indicatorlijst_naam=IndicatorlijstNamen.DOORLOOPTIJD_EN_KOSTEN
        )

        result = {}
        if indicatorlijst is not None:
            formulier = indicatorlijst.get_newest_formulier(year=year)
            if formulier is not None:
                result = formulier

        return result

    def __get_doorlooptijd_kosten_initieel(self) -> dict:
        formulier_initieel = self.__find_formulier(
            indicatorlijst_naam=IndicatorlijstNamen.DOORLOOPTIJD_EN_KOSTEN,
            indicator_titel=DoorlooptijdEnKosten.SOORT_ACTIE,
            indicator_waarde="Initieel",
        )

        if formulier_initieel is not None:
            return formulier_initieel
        else:
            # Sometimes there is no record with 'soort actie' = 'initieel', in that case find the oldest record.
            indicatorlijst = self.__get_indicatorlijst(
                indicatorlijst_naam=IndicatorlijstNamen.DOORLOOPTIJD_EN_KOSTEN
            )
            if indicatorlijst is not None:
                formulier_eerste = indicatorlijst.get_oldest_formulier(year=None)
                if formulier_eerste is not None:
                    return formulier_eerste
                else:
                    return {}
            else:
                return {}

    @property
    def redenen_herijking_str(self) -> str:
        herijkingen = []
        for herijking in self.toelichting_herijkingen:
            if herijking.get("Reden herijking") != "":
                herijkingen.append(str(herijking.get("Reden herijking")))
            else:
                herijkingen.append("Geen reden opgegeven")
        return ", ".join(herijkingen)

    @property
    def ontwikkelpartijen_str(self) -> str:
        ontwikkelpartijen = []
        for partij in self.toelichting_ontwikkelpartijen:
            ontwikkelpartij = partij.get(Ontwikkelpartijen.ONTWIKKELPARTIJ)
            if ontwikkelpartij != "":
                ontwikkelpartijen.append(ontwikkelpartij)
            else:
                ontwikkelpartijen.append("")
        return ", ".join(ontwikkelpartijen)

    @property
    def eindjaar(self) -> int | None:
        fixed_eindjaren = {
            # Aanbesteding applicatiediensten
            "673367a3-435c-4072-ba19-4a36528c3191": 2021,
            # Aanbesteding testdiensten
            "8d3320ac-9dc4-4275-ba9a-12d3868554e4": 2021,
            # DOOR
            "1dfb04b5-fbb4-463a-936d-b057c30a30f9": 2021,
            # Digitalisering Werkprocessen Bezwaar & Beroep
            "4625c3de-e659-438f-87c8-0b0992bcd08f": 2021,
        }

        fixed_eindjaar = fixed_eindjaren.get(self.project_id)

        if fixed_eindjaar is not None:
            return fixed_eindjaar
        elif self.__actueel_geschatte_einddatum is not None:
            return self.__actueel_geschatte_einddatum.year

    @property
    def dienstverlening(self) -> str:
        """
        Return dienstverlening as a string with values separated by ;.
        This is the default format used by the CMS for fields where multiple values can be selected.
        """

        indicatoren = ["Dienstverlening 1", "Dienstverlening 2", "Dienstverlening 3"]
        dienstverleningen = [
            self.indicatorlijst_algemeen_dict.get(i, None) for i in indicatoren
        ]

        heeft_dienstverlening_interne_bedrijfsvoering = (
            self.indicatorlijst_algemeen_dict.get("Interne bedrijfsvoering", None)
            == "Ja"
        )

        if heeft_dienstverlening_interne_bedrijfsvoering:
            dienstverleningen = dienstverleningen + ["Interne bedrijfsvoering"]

        unique_dienstverleningen = list(
            set([d for d in dienstverleningen if d is not None and len(d) > 0])
        )

        return ";".join(unique_dienstverleningen)

    def __get_project_summary_jbr(self) -> ProjectSamenvattingJBR:
        doorlooptijd_kosten_meest_recent = self.__doorlooptijd_kosten_meest_recent
        null_value = 0

        # If no year is specified, use the previous calendar year as the reference
        reference_year = (
            self.jbr_jaar if self.jbr_jaar is not None else datetime.date.today().year
        ) - 1

        dlt_kosten_meest_recent_vorig_jaar = (
            self.__get_doorlooptijd_kosten_meest_recent(year=reference_year)
        )
        doorlooptijd_kosten_initieel = self.__doorlooptijd_kosten_initieel

        schatting_totale_kosten_meest_recent = float(
            doorlooptijd_kosten_meest_recent.get(
                DoorlooptijdEnKosten.ACTUEEL_TOTAAL_PROJECTKOSTEN_CORRECT.value,
                null_value,
            ),
        )

        def parse_float(value: Any) -> float:
            try:
                if value == "":
                    return 0
                elif value is not None:
                    return float(value)
                else:
                    return value
            except ValueError as e:
                logger.error(f"Conversion error for value {str(value)}")
                raise e

        def get_cost_per_column(column: str) -> float:
            value = doorlooptijd_kosten_meest_recent.get(column, null_value)
            return parse_float(value)

        cumulatieve_kosten_vorig_jaar = dlt_kosten_meest_recent_vorig_jaar.get(
            DoorlooptijdEnKosten.DAADWERKELIJK_TOTAAL_PROJECTKOSTEN, null_value
        ) + dlt_kosten_meest_recent_vorig_jaar.get(
            DoorlooptijdEnKosten.DAADWERKELIJK_TOTAAL_PROJECTKOSTEN_NIEUW, null_value
        )

        cumulatieve_kosten_huidig_jaar = get_cost_per_column(
            DoorlooptijdEnKosten.DAADWERKELIJK_TOTAAL_PROJECTKOSTEN_CORRECT
        )

        doorlooptijd_actueel = get_timedelta_in_years(
            start=self.startdatum, end=self.__actueel_geschatte_einddatum
        )

        doorlooptijd_initieel = get_timedelta_in_years(
            start=self.startdatum, end=self.__initieel_geschatte_einddatum
        )

        return ProjectSamenvattingJBR(
            **{
                ActiviteitMetrics.ACTIVITEIT_ID: str(self.project_id),
                ActiviteitMetrics.MINISTERIE_AFKORTING: self.ministerie_afkorting,
                ActiviteitMetrics.ONDERWERP: self.indicatorlijst_algemeen_dict.get(
                    "Onderwerp", None
                ),
                ActiviteitMetrics.DIENSTVERLENING: self.dienstverlening,
                ActiviteitMetrics.SOORT: self.indicatorlijst_algemeen_dict.get(
                    "Soort ICT-activiteit", None
                ),
                ActiviteitMetrics.ONTWIKKELWIJZE: self.indicatorlijst_algemeen_dict.get(
                    "Ontwikkelwijze", None
                ),
                ActiviteitMetrics.BAAT: self.indicatorlijst_algemeen_dict.get(
                    "Maatschappelijk baat", None
                ),
                ActiviteitMetrics.NAAM: Formulier.parse_value(
                    self.naam, data_type=DataTypes.STRING
                ),
                ActiviteitMetrics.STARTDATUM: self.startdatum,
                ActiviteitMetrics.SCHATTING_EINDDATUM_INITIEEL: self.__initieel_geschatte_einddatum,
                ActiviteitMetrics.SCHATTING_EINDDATUM_ACTUEEL: self.__actueel_geschatte_einddatum,
                ActiviteitMetrics.SCHATTING_TOTALE_KOSTEN_INITIEEL: doorlooptijd_kosten_initieel.get(
                    DoorlooptijdEnKosten.ACTUEEL_TOTAAL_PROJECTKOSTEN_CORRECT.value,
                    null_value,
                ),
                ActiviteitMetrics.SCHATTING_TOTALE_KOSTEN_HUIDIG_JAAR: get_cost_per_column(
                    DoorlooptijdEnKosten.ACTUEEL_TOTAAL_PROJECTKOSTEN_CORRECT.value
                ),
                ActiviteitMetrics.SCHATTING_TOTALE_KOSTEN_VORIG_JAAR: dlt_kosten_meest_recent_vorig_jaar.get(
                    DoorlooptijdEnKosten.ACTUEEL_TOTAAL_PROJECTKOSTEN_CORRECT.value,
                    null_value,
                ),
                ActiviteitMetrics.DAADWERKELIJK_OVERIGE_KOSTEN: get_cost_per_column(
                    DoorlooptijdEnKosten.DAADWERKELIJK_OVERIGE_PROJECTKOSTEN
                ),
                ActiviteitMetrics.DAADWERKELIJK_EXTERN_PERSONEEL: get_cost_per_column(
                    DoorlooptijdEnKosten.DAADWERKELIJK_EXTERN_PERSONEEL_CORRECT
                ),
                ActiviteitMetrics.DAADWERKELIJK_INTERN_PERSONEEL: get_cost_per_column(
                    DoorlooptijdEnKosten.DAADWERKELIJK_INTERN_PERSONEEL_CORRECT
                ),
                ActiviteitMetrics.DAADWERKELIJK_UITBESTEED_WERK: get_cost_per_column(
                    DoorlooptijdEnKosten.DAADWERKELIJK_UITBESTEED_WERK
                ),
                ActiviteitMetrics.DAADWERKELIJK_INBESTEED_WERK: get_cost_per_column(
                    DoorlooptijdEnKosten.DAADWERKELIJK_INBESTEED_WERK
                ),
                ActiviteitMetrics.DAADWERKELIJK_DATAVERBINDINGEN: get_cost_per_column(
                    DoorlooptijdEnKosten.DAADWERKELIJK_DATAVERBINDINGEN
                ),
                ActiviteitMetrics.DAADWERKELIJK_STANDAARDSOFTWARE: get_cost_per_column(
                    DoorlooptijdEnKosten.DAADWERKELIJK_STANDAARDSOFTWARE
                ),
                ActiviteitMetrics.DAADWERKELIJK_HARDWARE: get_cost_per_column(
                    DoorlooptijdEnKosten.DAADWERKELIJK_HARDWARE
                ),
                ActiviteitMetrics.DAADWERKELIJK_HARDWARE_SOFTWARE: get_cost_per_column(
                    DoorlooptijdEnKosten.DAADWERKELIJK_HARDWARE_SOFTWARE
                ),
                ActiviteitMetrics.DAADWERKELIJK_OVERIG_MATERIEEL: get_cost_per_column(
                    DoorlooptijdEnKosten.DAADWERKELIJK_OVERIG_MATERIEEL_CORRECT
                ),
                ActiviteitMetrics.ACTUEEL_OVERIGE_KOSTEN: get_cost_per_column(
                    DoorlooptijdEnKosten.ACTUEEL_OVERIGE_PROJECTKOSTEN
                ),
                ActiviteitMetrics.ACTUEEL_EXTERN_PERSONEEL: get_cost_per_column(
                    DoorlooptijdEnKosten.ACTUEEL_EXTERN_PERSONEEL_CORRECT
                ),
                ActiviteitMetrics.ACTUEEL_INTERN_PERSONEEL: get_cost_per_column(
                    DoorlooptijdEnKosten.ACTUEEL_INTERN_PERSONEEL_CORRECT
                ),
                ActiviteitMetrics.ACTUEEL_UITBESTEED_WERK: get_cost_per_column(
                    DoorlooptijdEnKosten.ACTUEEL_UITBESTEED_WERK
                ),
                ActiviteitMetrics.ACTUEEL_INBESTEED_WERK: get_cost_per_column(
                    DoorlooptijdEnKosten.ACTUEEL_INBESTEED_WERK
                ),
                ActiviteitMetrics.ACTUEEL_DATAVERBINDINGEN: get_cost_per_column(
                    DoorlooptijdEnKosten.ACTUEEL_DATAVERBINDINGEN
                ),
                ActiviteitMetrics.ACTUEEL_STANDAARDSOFTWARE: get_cost_per_column(
                    DoorlooptijdEnKosten.ACTUEEL_STANDAARDSOFTWARE
                ),
                ActiviteitMetrics.ACTUEEL_HARDWARE: get_cost_per_column(
                    DoorlooptijdEnKosten.ACTUEEL_HARDWARE
                ),
                ActiviteitMetrics.ACTUEEL_HARDWARE_SOFTWARE: get_cost_per_column(
                    DoorlooptijdEnKosten.ACTUEEL_HARDWARE_SOFTWARE
                ),
                ActiviteitMetrics.ACTUEEL_OVERIG_MATERIEEL: get_cost_per_column(
                    DoorlooptijdEnKosten.ACTUEEL_GESCHAT_OVERIG_MATERIEEL_CORRECT
                ),
                ActiviteitMetrics.INITIEEL_OVERIGE_KOSTEN: parse_float(
                    doorlooptijd_kosten_initieel.get(
                        DoorlooptijdEnKosten.ACTUEEL_OVERIGE_PROJECTKOSTEN
                    )
                ),
                ActiviteitMetrics.INITIEEL_EXTERN_PERSONEEL: parse_float(
                    doorlooptijd_kosten_initieel.get(
                        DoorlooptijdEnKosten.ACTUEEL_EXTERN_PERSONEEL_CORRECT
                    )
                ),
                ActiviteitMetrics.INITIEEL_INTERN_PERSONEEL: parse_float(
                    doorlooptijd_kosten_initieel.get(
                        DoorlooptijdEnKosten.ACTUEEL_INTERN_PERSONEEL_CORRECT
                    )
                ),
                ActiviteitMetrics.INITIEEL_UITBESTEED_WERK: parse_float(
                    doorlooptijd_kosten_initieel.get(
                        DoorlooptijdEnKosten.ACTUEEL_UITBESTEED_WERK
                    )
                ),
                ActiviteitMetrics.INITIEEL_INBESTEED_WERK: parse_float(
                    doorlooptijd_kosten_initieel.get(
                        DoorlooptijdEnKosten.ACTUEEL_INBESTEED_WERK
                    )
                ),
                ActiviteitMetrics.INITIEEL_DATAVERBINDINGEN: parse_float(
                    doorlooptijd_kosten_initieel.get(
                        DoorlooptijdEnKosten.ACTUEEL_DATAVERBINDINGEN
                    )
                ),
                ActiviteitMetrics.INITIEEL_STANDAARDSOFTWARE: parse_float(
                    doorlooptijd_kosten_initieel.get(
                        DoorlooptijdEnKosten.ACTUEEL_STANDAARDSOFTWARE
                    )
                ),
                ActiviteitMetrics.INITIEEL_HARDWARE: parse_float(
                    doorlooptijd_kosten_initieel.get(
                        DoorlooptijdEnKosten.ACTUEEL_HARDWARE
                    )
                ),
                ActiviteitMetrics.INITIEEL_HARDWARE_SOFTWARE: parse_float(
                    doorlooptijd_kosten_initieel.get(
                        DoorlooptijdEnKosten.ACTUEEL_HARDWARE_SOFTWARE
                    )
                ),
                ActiviteitMetrics.INITIEEL_OVERIG_MATERIEEL: parse_float(
                    doorlooptijd_kosten_initieel.get(
                        DoorlooptijdEnKosten.ACTUEEL_GESCHAT_OVERIG_MATERIEEL_CORRECT
                    )
                ),
                ActiviteitMetrics.CUMULATIEVEKOSTEN_HUIDIG_JAAR: cumulatieve_kosten_huidig_jaar,
                ActiviteitMetrics.CUMULATIEVE_KOSTEN_VORIG_JAAR: cumulatieve_kosten_vorig_jaar,
                ActiviteitMetrics.PROGNOSE_TOEKOMSTIGE_KOSTEN: schatting_totale_kosten_meest_recent
                - cumulatieve_kosten_huidig_jaar,
                ActiviteitMetrics.STATUS: Formulier.parse_value(
                    self.projectstatus, data_type=DataTypes.STRING
                ),
                ActiviteitMetrics.ACTIEF_IN_JBR_JAAR: self.in_uitvoering_in_jbr_jaar,
                ActiviteitMetrics.MINISTERIE: self.ministerie_naam,
                ActiviteitMetrics.HEEFT_ACICT_ADVIES: self.heeft_acict_advies_gehad,
                ActiviteitMetrics.REDENEN_HERIJKINGEN: self.redenen_herijking_str,
                ActiviteitMetrics.AANTAL_BATEN: len(self.toelichting_baten),
                ActiviteitMetrics.ONTWIKKELPARTIJEN: self.ontwikkelpartijen_str,
                ActiviteitMetrics.AANTAL_BEHAALDE_MIJLPALEN: len(
                    self.toelichting_mijlpalen
                ),
                ActiviteitMetrics.AANTAL_ACICT_ADVIEZEN: len(self.acict_adviezen),
                ActiviteitMetrics.STARTJAAR: (
                    self.startdatum.year if self.startdatum else None
                ),
                ActiviteitMetrics.EINDJAAR: self.eindjaar,
                ActiviteitMetrics.DOORLOOPTIJD_ACTUEEL: doorlooptijd_actueel,
                ActiviteitMetrics.DOORLOOPTIJD_INITIEEL: doorlooptijd_initieel,
                ActiviteitMetrics.VERSCHIL_DOORLOOPTIJD_PCT: (
                    (doorlooptijd_actueel - doorlooptijd_initieel)
                    / doorlooptijd_initieel
                    if doorlooptijd_actueel is not None
                    and doorlooptijd_initieel is not None
                    and doorlooptijd_initieel != 0
                    else 0
                ),
                ActiviteitMetrics.VERSCHIL_EINDDATUM_INITIEEL_ACTUEEL_IN_JAREN: get_timedelta_in_years(
                    start=self.__initieel_geschatte_einddatum,
                    end=self.__actueel_geschatte_einddatum,
                ),
            }
        )

    def __get_indicatorlijst_summary(
        self,
        indicatorlijst_naam: IndicatorlijstNamen,
        information_columns: list[str],
        filter: IndicatorlijstFilter | None = None,
    ) -> list[dict]:
        """
        Returns a list of indicatorlijstformulieren based on the date column.
        If a date column is not defined, an empty list will be returned.

        Input:
        - indicatorlijst_naam: the name of the indicatorlijst
        - information_columns: a list of columns that need to be included in the returned list.
        """

        indicatorlijst = self.__get_indicatorlijst(
            indicatorlijst_naam=indicatorlijst_naam
        )

        if (
            indicatorlijst is not None
            and indicatorlijst.date_index_column is not None
            and indicatorlijst.date_index_column
            in list(indicatorlijst.formulieren_as_df.columns)
        ):
            df = indicatorlijst.formulieren_as_df
            has_valid_date_index_column = indicatorlijst.has_valid_date_index_column
            if has_valid_date_index_column:
                if self.jbr_jaar:
                    df_jaar = df.loc[
                        df[indicatorlijst.date_index_column].dt.year == self.jbr_jaar
                    ]
                else:
                    df_jaar = df

                if filter is not None:
                    df_jaar_filtered: pd.DataFrame = df_jaar.loc[
                        df_jaar[filter["indicatortitel"]] == filter["waarde"]
                    ]
                else:
                    df_jaar_filtered: pd.DataFrame = df_jaar

                available_information_columns = [
                    c
                    for c in information_columns
                    if c in list(df_jaar_filtered.columns)
                ]

                index_column: str = indicatorlijst.date_index_column
                df: pd.DataFrame = df_jaar_filtered.loc[
                    :, [index_column] + available_information_columns
                ]
                return df.sort_values(by=index_column, ascending=bool(False)).to_dict(
                    orient="records"
                )
            else:
                return []
        else:
            return []

    @property
    def heeft_acict_advies_gehad(self) -> Literal["Ja", "Nee"]:
        if len(self.acict_adviezen) > 0:
            return "Ja"
        else:
            return "Nee"

    @property
    def toelichting(self) -> dict:
        def format_dict(unformatted_dict: dict) -> dict:
            """
            Format a dictionary.

            Returns the original dictionary with formatted values.
            """
            for key in unformatted_dict.keys():
                value = unformatted_dict[key]
                if isinstance(value, list):
                    unformatted_dict[key] = [
                        format_dict(row) if isinstance(row, dict) else row
                        for row in value
                    ]
                elif isinstance(value, dict):
                    unformatted_dict[key] = format_dict(value)
                else:
                    if isinstance(value, datetime.datetime):
                        unformatted_dict[key] = value.date().strftime("%d-%m-%Y")
                    elif isinstance(value, datetime.date):
                        unformatted_dict[key] = value.strftime("%d-%m-%Y")

            return unformatted_dict

        toelichting = {
            "Algemeen": self.toelichting_samenvatting,
            # "Algemeen": self.indicatorlijst_algemeen_dict,
            "Kosten en uitgaven": self.toelichting_kosten_en_uitgaven,
            "Doorlooptijd": self.toelichting_doorlooptijd,
            "Ontwikkelpartijen": self.toelichting_ontwikkelpartijen,
            "Herijkingen": self.toelichting_herijkingen,
            "Mijlpalen": self.toelichting_mijlpalen,
            "Kwaliteitstoetsen": self.toelichting_kwaliteitstoetsen,
            "Tweede Kamerstukken": self.toelichting_tweedekamerstukken,
            "Meerwaarde per doelgroep": self.toelichting_baten,
        }

        return format_dict(toelichting)

    @property
    def toelichting_samenvatting(self) -> dict:
        indicatorlijst_peildatum_status = self.__get_indicatorlijst(
            indicatorlijst_naam=IndicatorlijstNamen.PEILDATUM_EN_STATUS
        )

        return {
            "Naam": self.naam,
            "Peildatum": (
                indicatorlijst_peildatum_status.formulieren_as_dict[0].get("Peildatum")
                if indicatorlijst_peildatum_status is not None
                else DEFAULT_DATE
            ),
            "Ministerie": self.ministerie_naam,
            "Samenwerkende ministerie(s)": self.indicatorlijst_algemeen_dict.get(
                "Samenwerkende ministerie(s)", "-"
            ),
            "Projectstatus": self.project_summary_jbr.ProjectStatus,
            "Onderwerp": self.indicatorlijst_algemeen_dict.get("Onderwerp", "-"),
            "Soort ICT-activiteit": self.indicatorlijst_algemeen_dict.get(
                "Soort ICT-activiteit", "-"
            ),
            "Ontwikkelwijze": self.indicatorlijst_algemeen_dict.get(
                "Ontwikkelwijze", "-"
            ),
            "Maatwerk": self.indicatorlijst_algemeen_dict.get("Maatwerk", "-"),
            "Heeft AcICT-advies gehad": self.heeft_acict_advies_gehad,
            "Dienstverlening 1": self.indicatorlijst_algemeen_dict.get(
                "Dienstverlening 1", "-"
            ),
            "Dienstverlening 2": self.indicatorlijst_algemeen_dict.get(
                "Dienstverlening 2", "-"
            ),
            "Dienstverlening 3": self.indicatorlijst_algemeen_dict.get(
                "Dienstverlening 3", "-"
            ),
            "Interne bedrijfsvoering": self.indicatorlijst_algemeen_dict.get(
                "Interne bedrijfsvoering", "-"
            ),
            "Maatschappelijk baat": self.project_summary_jbr.MaatschappelijkeBaat,
            "Aanleiding": self.indicatorlijst_algemeen_dict.get("Aanleiding", "-"),
            "Doelstelling": self.indicatorlijst_algemeen_dict.get("Doelstelling", "-"),
        }

    @property
    def toelichting_kosten_en_uitgaven(self) -> list[dict]:
        meest_recent = self.__doorlooptijd_kosten_meest_recent

        initieel = self.__doorlooptijd_kosten_initieel

        class Columns(str, Enum):
            SOORT_KOSTEN = "Soort kosten"
            INITIELE_INSCHATTING = "Initiële inschatting"
            ACTUELE_INSCHATTING = "Actuele inschatting"
            VERSCHIL = "Verschil"
            DAADWERKELIJKE_UITGAVEN = "Daadwerkelijke uitgaven"

        data = [
            {
                Columns.SOORT_KOSTEN.value: "Intern ICT-personeel",
                Columns.INITIELE_INSCHATTING.value: initieel.get(
                    DoorlooptijdEnKosten.ACTUEEL_INTERN_PERSONEEL_CORRECT
                ),
                Columns.ACTUELE_INSCHATTING.value: meest_recent.get(
                    DoorlooptijdEnKosten.ACTUEEL_INTERN_PERSONEEL_CORRECT
                ),
                Columns.VERSCHIL.value: meest_recent.get(
                    DoorlooptijdEnKosten.ACTUEEL_INTERN_PERSONEEL_CORRECT, 0
                )
                - initieel.get(
                    DoorlooptijdEnKosten.ACTUEEL_INTERN_PERSONEEL_CORRECT, 0
                ),
                Columns.DAADWERKELIJKE_UITGAVEN.value: meest_recent.get(
                    DoorlooptijdEnKosten.DAADWERKELIJK_INTERN_PERSONEEL_CORRECT
                ),
            },
            {
                Columns.SOORT_KOSTEN.value: "Extern ICT-personeel",
                Columns.INITIELE_INSCHATTING.value: initieel.get(
                    DoorlooptijdEnKosten.ACTUEEL_EXTERN_PERSONEEL_CORRECT
                ),
                Columns.ACTUELE_INSCHATTING.value: meest_recent.get(
                    DoorlooptijdEnKosten.ACTUEEL_EXTERN_PERSONEEL_CORRECT
                ),
                Columns.VERSCHIL.value: meest_recent.get(
                    DoorlooptijdEnKosten.ACTUEEL_EXTERN_PERSONEEL_CORRECT, 0
                )
                - initieel.get(
                    DoorlooptijdEnKosten.ACTUEEL_EXTERN_PERSONEEL_CORRECT, 0
                ),
                Columns.DAADWERKELIJKE_UITGAVEN.value: meest_recent.get(
                    DoorlooptijdEnKosten.DAADWERKELIJK_EXTERN_PERSONEEL_CORRECT
                ),
            },
            {
                Columns.SOORT_KOSTEN.value: "Materiele kosten",
                Columns.INITIELE_INSCHATTING.value: initieel.get(
                    DoorlooptijdEnKosten.ACTUEEL_GESCHAT_OVERIG_MATERIEEL_CORRECT
                ),
                Columns.ACTUELE_INSCHATTING.value: meest_recent.get(
                    DoorlooptijdEnKosten.ACTUEEL_GESCHAT_OVERIG_MATERIEEL_CORRECT
                ),
                Columns.VERSCHIL.value: round(
                    meest_recent.get(
                        DoorlooptijdEnKosten.ACTUEEL_GESCHAT_OVERIG_MATERIEEL_CORRECT, 0
                    )
                    - initieel.get(
                        DoorlooptijdEnKosten.ACTUEEL_GESCHAT_OVERIG_MATERIEEL_CORRECT, 0
                    ),
                    4,
                ),
                Columns.DAADWERKELIJKE_UITGAVEN.value: meest_recent.get(
                    DoorlooptijdEnKosten.DAADWERKELIJK_OVERIG_MATERIEEL_CORRECT, 0
                ),
            },
        ]

        df = pd.DataFrame(data).set_index(Columns.SOORT_KOSTEN.value)
        df.loc["Totaal"] = df.sum(numeric_only=True)

        df_with_na = df[df.isna().any(axis=1)]
        if len(df_with_na) > 0:
            for col in list(df_with_na.columns):
                if len(df[df[col].isna()]) > 0:
                    logger.debug(
                        f"{self.naam} has NaN-values in doorlooptijd en kosten for column {col}"
                    )
        df = df.fillna(0)

        return df.reset_index().to_dict(orient="records")

    @property
    def toelichting_doorlooptijd(self) -> dict:
        startdatum = self.project_summary_jbr.StartDatum
        einddatum_initieel = self.project_summary_jbr.SchattingEinddatumInitieel
        einddatum_actueel = self.__actueel_geschatte_einddatum

        delta = relativedelta(einddatum_actueel, einddatum_initieel)

        return {
            "StartDatum": startdatum,
            "SchattingEinddatumInitieel": einddatum_initieel,
            "SchattingEinddatumActueel": einddatum_actueel,
            "VerschilDoorlooptijdInMaanden": delta.months + delta.years * 12,
        }

    def __get_toelichting_ontwikkelpartijen(self) -> list[dict]:
        indicatorlijst = self.__get_indicatorlijst(
            indicatorlijst_naam=IndicatorlijstNamen.ONTWIKKELPARTIJEN
        )

        if indicatorlijst is not None:
            df = pd.DataFrame(
                indicatorlijst.formulieren_as_df[
                    [Ontwikkelpartijen.ONTWIKKELPARTIJ, Ontwikkelpartijen.ROL]
                ]
            )
            return df.to_dict(orient="records")
        else:
            return []

    def __get_toelichting_herijkingen(self) -> list[dict]:
        return self.__get_indicatorlijst_summary(
            indicatorlijst_naam=IndicatorlijstNamen.DOORLOOPTIJD_EN_KOSTEN,
            filter={
                "indicatortitel": DoorlooptijdEnKosten.SOORT_ACTIE,
                "waarde": "Herijking",
            },
            information_columns=[
                DoorlooptijdEnKosten.ACTUEEL_TOTAAL_PROJECTKOSTEN_CORRECT.value,
                DoorlooptijdEnKosten.ACTUEEL_GESCHATTE_EINDDATUM,
                DoorlooptijdEnKosten.REDEN_HERIJKING,
                DoorlooptijdEnKosten.TOELICHTING_WIJZIGING_KOSTEN,
                DoorlooptijdEnKosten.TOELICHTING_WIJZIGING_EINDDATUM,
            ],
        )

    def __get_toelichting_mijlpalen(self) -> list[dict]:
        return self.__get_indicatorlijst_summary(
            indicatorlijst_naam=IndicatorlijstNamen.MIJLPALEN,
            filter={
                "indicatortitel": Mijlpalen.MIJLPAAL_BEHAALD,
                "waarde": "Ja",
            },
            information_columns=[Mijlpalen.MIJLPAAL_OMSCHRIJVING],
        )

    @property
    def toelichting_kwaliteitstoetsen(self) -> list[dict]:
        return self.__get_indicatorlijst_summary(
            indicatorlijst_naam=IndicatorlijstNamen.KWALITEITSTOETSEN,
            information_columns=[
                Kwaliteitstoetsen.UITVOERENDE_PARTIJ,
                Kwaliteitstoetsen.SOORT_TOETS,
                Kwaliteitstoetsen.OMSCHRIJVING,
            ],
        )

    def __get_acict_adviezen(self) -> list[dict]:
        indicatorlijst = self.__get_indicatorlijst(
            indicatorlijst_naam=IndicatorlijstNamen.KWALITEITSTOETSEN
        )

        indicatorlijst_tk = self.__get_indicatorlijst(
            indicatorlijst_naam=IndicatorlijstNamen.TWEEDE_KAMERSTUKKEN
        )

        acict_adviezen_tk = (
            [
                f
                for f in indicatorlijst_tk.formulieren_as_dict
                if "ja" in f.get(TweedeKamerstukken.ACICT_ADVIES, "").lower()
                or "BIT" in f.get(TweedeKamerstukken.TITEL, "")
                or "adviescollege ict" in f.get(TweedeKamerstukken.TITEL, "").lower()
            ]
            if indicatorlijst_tk is not None
            else []
        )

        acict_adviezen_kwaliteitstoetsen = (
            [
                f
                for f in indicatorlijst.formulieren_as_dict
                if "bit" in f.get(Kwaliteitstoetsen.SOORT_TOETS, "").lower()
                or "ac-ict" in f.get(Kwaliteitstoetsen.SOORT_TOETS, "").lower()
                or "acict" in f.get(Kwaliteitstoetsen.SOORT_TOETS, "").lower()
            ]
            if indicatorlijst is not None
            else []
        )

        return acict_adviezen_tk + acict_adviezen_kwaliteitstoetsen

    @property
    def toelichting_tweedekamerstukken(self) -> list[dict]:
        return self.__get_indicatorlijst_summary(
            indicatorlijst_naam=IndicatorlijstNamen.TWEEDE_KAMERSTUKKEN,
            information_columns=[
                TweedeKamerstukken.NUMMER,
                TweedeKamerstukken.TITEL,
                TweedeKamerstukken.LINK,
            ],
        )

    def __get_toelichting_baten(self) -> list[dict]:
        indicatorlijst = self.__get_indicatorlijst(
            indicatorlijst_naam=IndicatorlijstNamen.MAATSCHAPPELIJKE_BATEN
        )

        if indicatorlijst is not None:
            return [f for f in indicatorlijst.formulieren_as_dict]
        else:
            return []
