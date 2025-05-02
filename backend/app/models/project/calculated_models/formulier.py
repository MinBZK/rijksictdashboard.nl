import datetime
from dataclasses import dataclass
from typing import Any

import app.schemas as schemas
from app.types import DataTypes, IndicatorlijstNamen
from app.types.indicatorlijst import DoorlooptijdEnKosten
from app.util.logger import get_logger


@dataclass
class CalculatedFormulierWaardeConfig:
    """
    The 'new' CMS has different field names for some formulieren.

    When a formulier is registered with the old CMS, but updated with the new CMS, there are fields with
    both the new name and the old name.

    In that case, only the new field should be selected. A new formulier value is created
    that selects the correct value.

    - title_preferred: if a formulier has a value with this title, use this value
    - title_alternative: if a formulier has no value for 'title preferred', use this value
    - title_corrected: the new formulier value uses this title
    """

    title_preferred: str
    titles_alternative: list[str]
    title_corrected: str


logger = get_logger(__name__)


@dataclass
class Formulier:
    """
    Args:
    - parsed_formulier_waardes
    - data_index_column
    - data_types
    - indicatortitels: lijst van alle indicatortitels per indicatorlijst. Niet elk formulier
        heeft dezelfde indicatortitels, waardoor datatypes verloren gaan als je het formulier
        omzet naar een DataFrame. Door gebruik te maken van alle indicatortitels wordt dit
        verholpen.

    """

    parsed_formulier_waardes: list[schemas.FormulierWaarde]
    date_index_column: str | None
    data_types: dict
    indicatortitels: list[str]
    indicatorlijstnaam: IndicatorlijstNamen

    def __post_init__(self):
        self.__apply_formulierwaarde_corrections()
        self.as_dict = self.__get_dict()

    @property
    def __corrections(self) -> list[CalculatedFormulierWaardeConfig]:
        if self.indicatorlijstnaam == IndicatorlijstNamen.DOORLOOPTIJD_EN_KOSTEN:
            return [
                CalculatedFormulierWaardeConfig(
                    title_preferred=DoorlooptijdEnKosten.ACTUEEL_TOTAAL_PROJECTKOSTEN_NIEUW,
                    titles_alternative=[
                        DoorlooptijdEnKosten.ACTUEEL_TOTAAL_PROJECTKOSTEN_OUD
                    ],
                    title_corrected=DoorlooptijdEnKosten.ACTUEEL_TOTAAL_PROJECTKOSTEN_CORRECT,
                ),
                CalculatedFormulierWaardeConfig(
                    title_preferred=DoorlooptijdEnKosten.ACTUEEL_EXTERN_PERSONEEL_NIEUW,
                    titles_alternative=[
                        DoorlooptijdEnKosten.ACTUEEL_EXTERN_PERSONEEL_OUD
                    ],
                    title_corrected=DoorlooptijdEnKosten.ACTUEEL_EXTERN_PERSONEEL_CORRECT,
                ),
                CalculatedFormulierWaardeConfig(
                    title_preferred=DoorlooptijdEnKosten.DAADWERKELIJK_EXTERN_PERSONEEL_NIEUW,
                    titles_alternative=[
                        DoorlooptijdEnKosten.DAADWERKELIJK_EXTERN_PERSONEEL_OUD
                    ],
                    title_corrected=DoorlooptijdEnKosten.DAADWERKELIJK_EXTERN_PERSONEEL_CORRECT,
                ),
                CalculatedFormulierWaardeConfig(
                    title_preferred=DoorlooptijdEnKosten.ACTUEEL_INTERN_PERSONEEL_NIEUW,
                    titles_alternative=[
                        DoorlooptijdEnKosten.ACTUEEL_INTERN_PERSONEEL_OUD
                    ],
                    title_corrected=DoorlooptijdEnKosten.ACTUEEL_INTERN_PERSONEEL_CORRECT,
                ),
                CalculatedFormulierWaardeConfig(
                    title_preferred=DoorlooptijdEnKosten.DAADWERKELIJK_INTERN_PERSONEEL_NIEUW,
                    titles_alternative=[
                        DoorlooptijdEnKosten.DAADWERKELIJK_INTERN_PERSONEEL_OUD
                    ],
                    title_corrected=DoorlooptijdEnKosten.DAADWERKELIJK_INTERN_PERSONEEL_CORRECT,
                ),
                CalculatedFormulierWaardeConfig(
                    title_preferred=DoorlooptijdEnKosten.DAADWERKELIJK_TOTAAL_PROJECTKOSTEN_NIEUW,
                    titles_alternative=[
                        DoorlooptijdEnKosten.DAADWERKELIJK_TOTAAL_PROJECTKOSTEN
                    ],
                    title_corrected=DoorlooptijdEnKosten.DAADWERKELIJK_TOTAAL_PROJECTKOSTEN_CORRECT,
                ),
                CalculatedFormulierWaardeConfig(
                    title_preferred=DoorlooptijdEnKosten.DAADWERKELIJK_OVERIG_MATERIEEL_NIEUW,
                    titles_alternative=[
                        DoorlooptijdEnKosten.DAADWERKELIJK_DATAVERBINDINGEN,
                        DoorlooptijdEnKosten.DAADWERKELIJK_HARDWARE,
                        DoorlooptijdEnKosten.DAADWERKELIJK_HARDWARE_SOFTWARE,
                        DoorlooptijdEnKosten.DAADWERKELIJK_INBESTEED_WERK,
                        DoorlooptijdEnKosten.DAADWERKELIJK_OVERIGE_PROJECTKOSTEN,
                        DoorlooptijdEnKosten.DAADWERKELIJK_STANDAARDSOFTWARE,
                        DoorlooptijdEnKosten.DAADWERKELIJK_UITBESTEED_WERK,
                    ],
                    title_corrected=DoorlooptijdEnKosten.DAADWERKELIJK_OVERIG_MATERIEEL_CORRECT,
                ),
                CalculatedFormulierWaardeConfig(
                    title_preferred=DoorlooptijdEnKosten.ACTUEEL_GESCHAT_OVERIG_MATERIEEL_NIEUW,
                    titles_alternative=[
                        DoorlooptijdEnKosten.ACTUEEL_DATAVERBINDINGEN,
                        DoorlooptijdEnKosten.ACTUEEL_HARDWARE,
                        DoorlooptijdEnKosten.ACTUEEL_HARDWARE_SOFTWARE,
                        DoorlooptijdEnKosten.ACTUEEL_INBESTEED_WERK,
                        DoorlooptijdEnKosten.ACTUEEL_OVERIGE_PROJECTKOSTEN,
                        DoorlooptijdEnKosten.ACTUEEL_STANDAARDSOFTWARE,
                        DoorlooptijdEnKosten.ACTUEEL_UITBESTEED_WERK,
                    ],
                    title_corrected=DoorlooptijdEnKosten.ACTUEEL_GESCHAT_OVERIG_MATERIEEL_CORRECT,
                ),
            ]
        else:
            return []

    def __get_formulier_value_by_title(self, target_title: str):
        formulier_waarde = next(
            (
                fw
                for fw in self.parsed_formulier_waardes
                if fw.IndicatorTitel == target_title
            ),
            None,
        )
        if formulier_waarde:
            return formulier_waarde.Waarde

    def __apply_formulierwaarde_corrections(self):
        def __return_zero_if_none(v: Any) -> float | int:
            if isinstance(v, float) or isinstance(v, int):
                return v
            elif v is not None:
                return float(v)
            elif v is None:
                return 0
            else:
                return v

        def __get_best_value(correction: CalculatedFormulierWaardeConfig):
            v_preferred = __return_zero_if_none(
                self.__get_formulier_value_by_title(correction.title_preferred)
            )
            v_alternative = sum(
                [
                    __return_zero_if_none(self.__get_formulier_value_by_title(t))
                    for t in correction.titles_alternative
                ]
            )
            return v_preferred if v_preferred > 0 else v_alternative

        max_indicator_index = max(
            [fw.IndicatorIndex for fw in self.parsed_formulier_waardes]
        )

        for c in self.__corrections:
            self.parsed_formulier_waardes.insert(
                0,
                schemas.FormulierWaarde(
                    IndicatorTitel=c.title_corrected,
                    IndicatorIndex=max_indicator_index + 1,
                    IndicatorAntwoordTypeNaam="Calculated value",
                    Waarde=str(__get_best_value(c)),
                ),
            )
            max_indicator_index = max_indicator_index + 1

    def __get_dict(self) -> dict:
        def get_data_type(indicatortitel: str) -> DataTypes:
            configured_data_type = self.data_types.get(indicatortitel)
            if configured_data_type is not None:
                return configured_data_type
            else:
                return DataTypes.STRING

        formulier_as_dict = {
            fw.IndicatorTitel: self.parse_value(
                waarde=fw.Waarde,
                data_type=get_data_type(fw.IndicatorTitel),
            )
            for fw in self.parsed_formulier_waardes
        }

        existing_indicatortitels = formulier_as_dict.keys()
        missing_indicatortitels = [
            it for it in self.indicatortitels if it not in existing_indicatortitels
        ]

        missing_values_dict = {
            indicatortitel: self.parse_value(
                waarde=None,
                data_type=get_data_type(indicatortitel),
            )
            for indicatortitel in missing_indicatortitels
        }

        return {**formulier_as_dict, **missing_values_dict}

    @classmethod
    def parse_value(
        cls, waarde: str | None, data_type: DataTypes
    ) -> str | float | int | datetime.date | None:
        result = None

        if data_type == DataTypes.FLOAT and waarde is not None:
            result = float(waarde)
        elif data_type == DataTypes.FLOAT and waarde is None:
            result = 0
        elif data_type == DataTypes.DATE and waarde is not None:
            try:
                return datetime.datetime.strptime(waarde, "%Y-%m-%d")
            except Exception:
                result = None
        elif data_type == DataTypes.DATE and waarde is None:
            result = None
        elif waarde is not None:
            result = waarde
        else:
            result = ""

        return result
