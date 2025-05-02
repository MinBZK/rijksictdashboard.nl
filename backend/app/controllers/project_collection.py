from __future__ import annotations

import itertools
import re
from collections import Counter
from typing import Any, Dict, Hashable, Literal

import numpy as np
import pandas as pd

import app.controllers.ict_kosten as ict_kosten
from app.config.indicatorlijst import attributes_with_multiple_values
from app.models.project.core import ProjectViewMetWaardes
from app.schemas.project import Project
from app.services import ProjectGetter
from app.store import store
from app.types import ActiviteitMetrics, Ontwikkelpartijen, ProjectFilter, Projectstatus
from app.util.logger import get_logger

logger = get_logger(__name__)


class ProjectCollection:
    def __init__(
        self,
        filters: list[ProjectFilter] = [],
        year: int | None = None,
        search_activiteit_naam: str | None = None,
        activiteit_id: str | None = None,
        status: list[Projectstatus] | None = None,
        included_ids_forced: list[str] = [],
        include_nog_niet_gestart: bool = False,
    ):
        self.__activiteit_id = activiteit_id
        self.__year = year
        self.__status = status if status is not None else []
        self.__filters = [f for f in filters if len(f.values) > 0]
        self.__search_activiteit_naam = search_activiteit_naam
        self.__included_ids_forced = included_ids_forced
        self.__include_nog_niet_gestart = include_nog_niet_gestart

        self.projecten_unfiltered = []
        getter = (
            ProjectGetter() if year is not None else store.activiteiten_current.get()
        )

        self.projecten_unfiltered = [p for p in getter.projecten]
        if year is not None:
            for p in self.projecten_unfiltered:
                p.set_calculated_attributes(year=year)
        self.project_dict = {str(p.ProjectId): p for p in self.projecten_unfiltered}

        self.projecten_filtered = self.get_projecten_filtered(filters=self.__filters)
        self.__projecten_df_filtered = self.get_projecten_df(
            projecten=self.projecten_filtered
        )
        self.__ict_kosten_most_recent = max(ict_kosten.get_years())

    def get_projecten_filtered(self, filters: list[ProjectFilter]):
        def project_in_scope(p: ProjectViewMetWaardes) -> bool:
            exclude_on_id = (
                p.ProjectId != self.__activiteit_id and self.__activiteit_id is not None
            )

            exclude_on_peildatum = (
                self.__year is not None
                and not p.calculated_attributes.in_uitvoering_in_jbr_jaar
            )

            exclude_on_status = (
                p.ProjectStatus not in self.__status
                and len(self.__status) > 0
                or (
                    p.ProjectStatus == Projectstatus.NOG_NIET_GESTART.value
                    and not self.__include_nog_niet_gestart
                )
            )

            def get_attribute(project: ProjectViewMetWaardes, attribute: str) -> Any:
                v = getattr(project.merged_attributes, attribute)
                return v if v is not None else ""

            # exclude on filters
            exclude_on_filters = (
                not all(
                    [
                        (
                            getattr(p.merged_attributes, f.attribute) in f.values
                            if f.attribute not in attributes_with_multiple_values
                            else any(
                                [
                                    v in f.values
                                    for v in get_attribute(p, f.attribute).split(";")
                                ]
                            )
                        )
                        for f in filters
                    ]
                )
                and len(filters) > 0
            )
            exclude_on_name = (
                self.__search_activiteit_naam is not None
                and self.__search_activiteit_naam.lower() not in p.Naam.lower()
            )

            exclusions = [
                exclude_on_id,
                exclude_on_peildatum,
                exclude_on_status,
                exclude_on_filters,
                exclude_on_name,
            ]

            include_project = (
                not any(exclusions) or p.ProjectId in self.__included_ids_forced
            )

            manually_included_in_2023 = self.__year == 2023 and p.ProjectId in [
                "76e94913-ea32-4340-8558-76db00b0cea3",
                "54a06bb5-8f8e-4d16-9a8b-244863d86179",
                "90feca20-8f9b-483a-9934-071976b98c47",
                "feae74c8-4322-4a19-b4b3-4a3cec5b5c13",
                "1e705368-d04e-4013-9fca-90632489bbb6",
                "99672c8c-223d-4a7d-9d63-2a0e5eb12ceb",
                "0ef287f7-dc23-4f8d-847f-9690b64b00da",
                "32ef0a4a-fe19-44c1-af14-fdca5abdf013",
                "df0039b7-e798-40a4-982f-3b4f4b04e6d9",
                "83bf8006-57a6-4537-a1fc-85db2458e082",
            ]

            return include_project or manually_included_in_2023

        filtered_projecten = [
            p for p in self.projecten_unfiltered if project_in_scope(p)
        ]

        return filtered_projecten

    @property
    def ministeries(self) -> list[str]:
        return list(set([p.MinisterieNaam for p in self.projecten_unfiltered]))

    @property
    def __aantal_afgeronde_activiteiten(self) -> int:
        return len(
            [
                p
                for p in self.projecten_unfiltered
                if p.ProjectStatus == Projectstatus.AFGEROND.value
            ]
        )

    @property
    def __aantal_gestart_en_afgerond(self) -> list[dict[Hashable, Any]]:
        df = self.__projecten_df_filtered
        start = (
            (
                df.groupby(["StartJaar"])["ActiviteitId"]
                .count()
                .reset_index()
                .rename(
                    columns={
                        "StartJaar": "x",
                        "ActiviteitId": "y",
                        ActiviteitMetrics.STATUS.value: "label",
                    }
                )
                .to_dict(orient="records")
            )
            if len(df) > 0
            else []
        )
        for row in start:
            row["label"] = "Nieuw"

        eind = (
            (
                df[
                    df[ActiviteitMetrics.STATUS.value].isin(
                        [Projectstatus.AFGEROND.value, Projectstatus.GEANNULEERD.value]
                    )
                ]
                .groupby(["EindJaar", ActiviteitMetrics.STATUS.value])[
                    ActiviteitMetrics.ACTIVITEIT_ID.value
                ]
                .count()
                .reset_index()
                .rename(
                    columns={
                        "EindJaar": "x",
                        ActiviteitMetrics.ACTIVITEIT_ID.value: "y",
                        ActiviteitMetrics.STATUS.value: "label",
                    }
                )
                .to_dict(orient="records")
            )
            if len(df) > 0
            else []
        )

        return start + eind

    def __count_category(self, category: str) -> dict:
        if category in list(self.__projecten_df_filtered.columns):
            return self.__projecten_df_filtered[category].value_counts().to_dict()
        else:
            return {}

    def __sum_columns(
        self,
        columns: list[ActiviteitMetrics],
        column_mapping: dict | None = None,
    ) -> dict[str, float]:
        df = self.__projecten_df_filtered
        matched_columns = [c for c in columns if c in list(df.columns)]

        return (
            df[matched_columns]
            .rename(columns=column_mapping if column_mapping else {})  # type: ignore
            .sum()
            .to_dict()
        )

    def get_project_by_id(self, activiteit_id: str) -> ProjectViewMetWaardes | None:
        return self.project_dict.get(activiteit_id, None)

    @property
    def aantal_activiteiten_gestart(self) -> dict:
        return self.__count_category(category=ActiviteitMetrics.STARTDATUM)

    @property
    def aantal_activiteiten_afgerond(self) -> dict:
        return self.__count_category(
            category=ActiviteitMetrics.SCHATTING_EINDDATUM_ACTUEEL
        )

    @property
    def __verschil_kosten_schatting_percentage(self) -> float:
        df = self.__projecten_df_filtered
        kosten_actueel = ActiviteitMetrics.SCHATTING_TOTALE_KOSTEN_HUIDIG_JAAR
        kosten_initieel = ActiviteitMetrics.SCHATTING_TOTALE_KOSTEN_INITIEEL

        if kosten_actueel in list(df.columns) and kosten_initieel in list(df.columns):
            kosten_actueel = df[kosten_actueel].sum()
            kosten_initieel = df[kosten_initieel].sum()
            return (
                (kosten_actueel - kosten_initieel) / kosten_initieel
                if kosten_initieel > 0
                else 0
            ) * 100
        else:
            return 0

    @property
    def __herijking_redenen(self) -> dict[str, int]:
        """
        Returns a dictionary that counts the occurance of each value in the column 'reden herijking'
        """
        indicatortitel = "Reden herijking"
        redenen_per_project = [
            reden
            for p in self.projecten_filtered
            for herijking in p.calculated_attributes.toelichting_herijkingen
            for reden in re.split(";|,", herijking.get(indicatortitel, ""))
            if reden != "" and herijking.get(indicatortitel) != ""
        ]
        return dict(Counter(redenen_per_project))

    @property
    def __totaal_aantal_baten(self) -> int:
        return sum(
            [
                len(p.calculated_attributes.toelichting_baten)
                for p in self.projecten_filtered
            ]
        )

    @property
    def __aantal_ict_activiteiten_met_baten(self) -> int:
        return len(
            [
                p
                for p in self.projecten_filtered
                if len(p.calculated_attributes.toelichting_baten) > 0
            ]
        )

    @property
    def __ontwikkelpartijen(self) -> Dict[str, int]:
        df = pd.DataFrame(
            itertools.chain(
                *[
                    p.calculated_attributes.toelichting_ontwikkelpartijen
                    for p in self.projecten_filtered
                ]
            )
        )
        return (
            df[Ontwikkelpartijen.ONTWIKKELPARTIJ].value_counts().to_dict()
            if len(df) > 0
            else {}
        )

    @property
    def __aantal_behaalde_mijlpalen(self) -> int:
        return sum(
            [
                len(p.calculated_attributes.toelichting_mijlpalen)
                for p in self.projecten_filtered
            ]
        )

    @property
    def __aantal_acict_toetsen(self) -> int:
        """
        Bereken het aantal projecten dat minimaal 1 AcICT-advies heeft gehad.
        """
        return len(
            [
                p
                for p in self.projecten_filtered
                if p.calculated_attributes.heeft_acict_advies_gehad == "Ja"
            ]
        )

    @property
    def __top_3_recent_toegevoegde_activiteiten(self) -> list[Project]:
        """
        Returns the top 3 recent projects based on metric.
        """
        projecten = [p for p in self.projecten_unfiltered if p.ProjectVersie == 0]
        sorted_projecten = sorted(
            projecten,
            key=lambda p: p.ProjectVersieWijzigingsDatum,
            reverse=True,
        )
        return [Project.model_validate(p) for p in sorted_projecten[:3]]

    @property
    def __top_3_recent_afgeronde_activiteiten(self) -> list[Project]:
        """
        Returns the top 3 recent projects based on metric.
        """
        projecten = [
            p
            for p in self.projecten_unfiltered
            if p.ProjectStatus == Projectstatus.AFGEROND.value
        ]

        sorted_projecten = sorted(
            projecten,
            key=lambda p: p.ProjectVersieWijzigingsDatum,
            reverse=True,
        )
        return [Project.model_validate(p) for p in sorted_projecten[:3]]

    @property
    def projecten(self) -> dict[str, list[Project]]:
        """
        Returns a list of projects.
        """
        return {
            "Top 3 recent toegevoegde ICT-activiteiten": self.__top_3_recent_toegevoegde_activiteiten,
            "Top 3 recent afgeronde ICT-activiteiten": self.__top_3_recent_afgeronde_activiteiten,
        }

    @property
    def __daadwerkelijke_uitgaven_per_categorie(self) -> dict[str, float]:
        columns_to_be_aggregated = [
            ActiviteitMetrics.DAADWERKELIJK_OVERIGE_KOSTEN,
            ActiviteitMetrics.DAADWERKELIJK_EXTERN_PERSONEEL,
            ActiviteitMetrics.DAADWERKELIJK_INTERN_PERSONEEL,
            ActiviteitMetrics.DAADWERKELIJK_UITBESTEED_WERK,
            ActiviteitMetrics.DAADWERKELIJK_INBESTEED_WERK,
            ActiviteitMetrics.DAADWERKELIJK_DATAVERBINDINGEN,
            ActiviteitMetrics.DAADWERKELIJK_STANDAARDSOFTWARE,
            ActiviteitMetrics.DAADWERKELIJK_HARDWARE,
            ActiviteitMetrics.DAADWERKELIJK_HARDWARE_SOFTWARE,
            ActiviteitMetrics.DAADWERKELIJK_OVERIG_MATERIEEL,
        ]
        return self.__sum_columns(columns=columns_to_be_aggregated)

    @property
    def __actuele_uitgaven_per_categorie(self) -> Dict[str, float]:
        columns_to_be_aggregated = [
            ActiviteitMetrics.ACTUEEL_OVERIGE_KOSTEN,
            ActiviteitMetrics.ACTUEEL_EXTERN_PERSONEEL,
            ActiviteitMetrics.ACTUEEL_INTERN_PERSONEEL,
            ActiviteitMetrics.ACTUEEL_UITBESTEED_WERK,
            ActiviteitMetrics.ACTUEEL_INBESTEED_WERK,
            ActiviteitMetrics.ACTUEEL_DATAVERBINDINGEN,
            ActiviteitMetrics.ACTUEEL_STANDAARDSOFTWARE,
            ActiviteitMetrics.ACTUEEL_HARDWARE,
            ActiviteitMetrics.ACTUEEL_HARDWARE_SOFTWARE,
            ActiviteitMetrics.ACTUEEL_OVERIG_MATERIEEL,
        ]
        return self.__sum_columns(columns=columns_to_be_aggregated)

    @property
    def __meerjarige_kosten(self) -> dict:
        columns_to_be_summed = {
            ActiviteitMetrics.SCHATTING_TOTALE_KOSTEN_INITIEEL: "Initieel geschatte meerjarige projectkosten",
            ActiviteitMetrics.SCHATTING_TOTALE_KOSTEN_HUIDIG_JAAR: "Geschatte meerjarige projectkosten",
            ActiviteitMetrics.CUMULATIEVEKOSTEN_HUIDIG_JAAR: "Daadwerkelijke uitgaven",
            ActiviteitMetrics.PROGNOSE_TOEKOMSTIGE_KOSTEN: "Prognose toekomstige kosten",
        }

        return self.__sum_columns(
            columns=[c for c in columns_to_be_summed.keys()],
            column_mapping=columns_to_be_summed,
        )

    @property
    def activiteit_overzicht(self) -> pd.DataFrame:
        if len(self.__projecten_df_filtered) > 0:
            df = self.__projecten_df_filtered.sort_values(
                by=[ActiviteitMetrics.MINISTERIE_AFKORTING, ActiviteitMetrics.NAAM],
                key=lambda col: col.str.lower(),
            )
        else:
            df = self.__projecten_df_filtered
        columns = list(df.columns)
        df[ActiviteitMetrics.NUMMER.value] = range(1, len(df) + 1)
        if len(columns) > 0:
            df = df.loc[:, [ActiviteitMetrics.NUMMER.value] + columns]

        for c in df.select_dtypes(include=["datetime64"]).columns:
            df[c] = df[c].dt.strftime("%d-%m-%Y")

        excluded_columns = [ActiviteitMetrics.ACTIEF_IN_JBR_JAAR]
        if len(df) > 0:
            df = df.drop(columns=excluded_columns)
        return df

    @property
    def kengetallen(self) -> dict[str | Hashable, float | Any]:
        aggregations: dict[ActiviteitMetrics, Literal["sum", "mean"]] = {
            ActiviteitMetrics.SCHATTING_TOTALE_KOSTEN_INITIEEL: "sum",
            ActiviteitMetrics.SCHATTING_TOTALE_KOSTEN_HUIDIG_JAAR: "sum",
            ActiviteitMetrics.CUMULATIEVEKOSTEN_HUIDIG_JAAR: "sum",
            ActiviteitMetrics.PROGNOSE_TOEKOMSTIGE_KOSTEN: "sum",
            ActiviteitMetrics.DOORLOOPTIJD_ACTUEEL: "mean",
            ActiviteitMetrics.DOORLOOPTIJD_INITIEEL: "mean",
            ActiviteitMetrics.AANTAL_BEHAALDE_MIJLPALEN: "sum",
        }

        def get_aggregated_column_name(
            column_name: ActiviteitMetrics, aggregation: str
        ) -> str:
            return f"{column_name.value} ({aggregation})"

        if len(self.__projecten_df_filtered) > 0:
            aggregated_columns = (
                self.__projecten_df_filtered.agg(aggregations)
                .rename(
                    {
                        k: get_aggregated_column_name(k, v)
                        for k, v in aggregations.items()
                    }
                )
                .to_dict()
            )
        else:
            aggregated_columns = {
                get_aggregated_column_name(k, v): 0 for k, v in aggregations.items()
            }

        doorlooptijd_aantallen = {
            category: count
            for category, count in self.__count_category(
                category=ActiviteitMetrics.EINDDATUM_EERDER_LATER.value
            ).items()
            if category != "Doorlooptijd onbekend"
        }

        return {
            "Aantal grote ICT-activiteiten": len(self.__projecten_df_filtered.index),
            "Aantal ICT projecten per status": self.__count_category(
                category=ActiviteitMetrics.STATUS
            ),
            "Doorlooptijd (aantallen)": doorlooptijd_aantallen,
            "Doorlooptijd (%)": self.__count_category(
                category=ActiviteitMetrics.DOORLOOPTIJD_EERDER_LATER_PCT.value
            ),
            "Geschatte kosten per categorie": self.__count_category(
                category=ActiviteitMetrics.TOTALE_KOSTEN_CATEGORIE.value
            ),
            "Geschatte kosten verschil in %": self.__verschil_kosten_schatting_percentage,
            "Herijkingen aantal per redenen": self.__herijking_redenen,
            "Daadwerkelijke uitgaven": self.__daadwerkelijke_uitgaven_per_categorie,
            "Actuele uitgaven": self.__actuele_uitgaven_per_categorie,
            "Meerjarige kosten": self.__meerjarige_kosten,
            "Totaal aantal baten": self.__totaal_aantal_baten,
            "Aantal activiteiten met baten": self.__aantal_ict_activiteiten_met_baten,
            "Aantal behaalde mijlpalen": self.__aantal_behaalde_mijlpalen,
            "Ontwikkelpartijen": self.__ontwikkelpartijen,
            "Aantal AcICT-adviezen": self.__aantal_acict_toetsen,
            "Aantal gestarte activiteiten": self.__aantal_gestart_en_afgerond,
            "Aantal afgeronde activiteiten": self.__aantal_afgeronde_activiteiten,
            "Meest recente jaar met kosten": self.__ict_kosten_most_recent,
            **aggregated_columns,  # type: ignore
        }

    def get_projecten_met_toelichting(self) -> list[dict]:
        return [
            project.calculated_attributes.toelichting
            for project in self.projecten_filtered
        ]

    def get_projecten_df(self, projecten: list[ProjectViewMetWaardes]) -> pd.DataFrame:
        """
        Returns dataframe with active projects.
        """

        df = pd.DataFrame(
            [
                p.calculated_attributes.project_summary_jbr.model_dump()
                for p in projecten
            ]
        )

        n_activiteiten = len(df.index)

        if n_activiteiten > 0:
            # toevoegen kolom met verschil tussen initiele en actuele einddatum categorie
            verschil = (
                ActiviteitMetrics.VERSCHIL_EINDDATUM_INITIEEL_ACTUEEL_IN_JAREN.value
            )
            df[ActiviteitMetrics.EINDDATUM_EERDER_LATER.value] = np.where(
                df[verschil] < 0,
                "Eerder",
                np.where(
                    df[verschil] == 0,
                    "Ongewijzigd",
                    np.where(
                        (df[verschil] > 0) & (df[verschil] <= 1),
                        "Later ≤1 jaar",
                        np.where(
                            df[verschil] > 1, "Later >1 jaar", "Doorlooptijd onbekend"
                        ),
                    ),
                ),
            )

            # toevoegen kolom verschil initiele en actuele doorlooptijd in %
            verschil_perc = ActiviteitMetrics.VERSCHIL_DOORLOOPTIJD_PCT.value

            # toevoegen kolom categoerie verschil initele em actuele doorlooptijd in %
            df[ActiviteitMetrics.DOORLOOPTIJD_EERDER_LATER_PCT.value] = np.where(
                df[verschil_perc] < 0,
                "Eerder",
                np.where(
                    df[verschil_perc] == 0,
                    "Ongewijzigd",
                    np.where(
                        (df[verschil_perc] > 0) & (df[verschil_perc] < 0.5),
                        "Later < 50%",
                        np.where(
                            (df[verschil_perc] >= 0.5) & (df[verschil_perc] < 1),
                            "Later 50-100%",
                            np.where(
                                df[verschil_perc] >= 1,
                                "Later >= 100%",
                                "Doorlooptijd onbekend",
                            ),
                        ),
                    ),
                ),
            )

            # toevoegen kolom totale kosten categorie
            geschatte_kosten = ActiviteitMetrics.SCHATTING_TOTALE_KOSTEN_HUIDIG_JAAR
            bins = [0, 10, 20, 30, 40, 50, 100, float("inf")]
            labels = [
                "0-10 mln.",
                "10-20 mln.",
                "20-30 mln.",
                "30-40 mln.",
                "40-50 mln.",
                "50-100 mln.",
                "100+ mln.",
            ]
            na_category = "(Geen kosten bekend)"

            if geschatte_kosten in list(df.columns):
                category_bin = ActiviteitMetrics.TOTALE_KOSTEN_CATEGORIE.value
                df[category_bin] = pd.cut(
                    df[geschatte_kosten.value], bins=bins, labels=labels, ordered=True
                )
                df[category_bin] = (
                    df[category_bin].cat.add_categories(na_category).fillna(na_category)
                )

        return df
