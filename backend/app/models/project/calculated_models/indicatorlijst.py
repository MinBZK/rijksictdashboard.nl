from dataclasses import dataclass
from typing import Any

import pandas as pd

import app.schemas as schemas
from app.config.indicatorlijst import IndicatorlijstConfig, indicatorlijst_config
from app.types import DataTypes, IndicatorlijstColumn, IndicatorlijstNamen
from app.util.logger import get_logger

from .formulier import Formulier

logger = get_logger(__name__)


@dataclass
class Indicatorlijst:
    parsed_indicatorlijst: schemas.IndicatorLijst
    naam: IndicatorlijstNamen
    project_naam: str

    def __post_init__(self):
        self.indicatortitels = self.__get_indicatortitels()
        self.formulieren = self.__get_formulieren()
        self.formulieren_as_dict = self.__get_formulieren_as_dict()
        self.formulieren_as_df = self.__get_formulieren_as_df()
        self.has_valid_date_index_column = self.__check_date_index_validity()

    def __get_first_formulier(
        self, year: int | None, sort_date_ascending: bool
    ) -> dict | None:
        if self.date_index_column is None:
            error = f"Indicatorlijst {self.naam} expected to have a date column that is not None"  # noqa: E501
            raise ValueError(error)

        # get indicatorlijst as dataframe
        df = self.formulieren_as_df

        if not self.has_valid_date_index_column:
            logger.error(
                f"No valid date index column for {self.naam} in {self.project_naam}"
            )

        # only get values up until requested year
        if year is not None and self.has_valid_date_index_column:
            df_filtered: pd.DataFrame = df.loc[
                df[self.date_index_column].dt.year <= year
            ]
        else:
            df_filtered: pd.DataFrame = df

        if self.has_valid_date_index_column:
            df_sorted = df_filtered.sort_values(
                by=self.date_index_column, ascending=sort_date_ascending
            )
        else:
            df_sorted = df_filtered

        # get most recent value of requested year
        if len(df_sorted.index) > 0:
            return df_sorted.to_dict(orient="records")[0]

    def get_newest_formulier(self, year: int | None) -> dict | None:
        return self.__get_first_formulier(year=year, sort_date_ascending=False)

    def get_oldest_formulier(self, year: int | None) -> dict | None:
        return self.__get_first_formulier(year=year, sort_date_ascending=True)

    def __get_formulieren_as_dict(self) -> list[dict[str, Any]]:
        return [f.as_dict for f in self.formulieren]

    def __get_formulieren(self) -> list[Formulier]:
        return [
            Formulier(
                parsed_formulier_waardes=f.FormulierWaardes,
                date_index_column=self.date_index_column,
                data_types=self.data_types,
                indicatortitels=self.indicatortitels,
                indicatorlijstnaam=self.naam,
            )
            for f in self.parsed_indicatorlijst.Formulier
        ]

    def __get_indicatortitels(self) -> list[str]:
        return [
            w.IndicatorTitel
            for f in self.parsed_indicatorlijst.Formulier
            for w in f.FormulierWaardes
        ]

    def __get_formulieren_as_df(self) -> pd.DataFrame:
        df = pd.DataFrame(self.formulieren_as_dict)
        return df

    @property
    def config(self) -> IndicatorlijstConfig | None:
        return indicatorlijst_config.get(self.naam)

    @property
    def date_index_column(self) -> str | None:
        return self.config["date_index_column"] if self.config is not None else None

    @property
    def data_types(self) -> dict[IndicatorlijstColumn, DataTypes]:
        return self.config["data_types"] if self.config is not None else {}

    def __check_date_index_validity(self) -> bool:
        if self.date_index_column and self.date_index_column in list(
            self.formulieren_as_df.columns
        ):
            return (
                self.formulieren_as_df[self.date_index_column].dtype == "datetime64[ns]"
            )
        else:
            return False
