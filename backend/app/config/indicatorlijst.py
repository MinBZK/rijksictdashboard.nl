from typing import TypedDict

from app.types import (
    ActiviteitMetrics,
    DataTypes,
    # Indicatorlijsten
    DoorlooptijdEnKosten,
    IndicatorlijstColumn,
    IndicatorlijstNamen,
    Kwaliteitstoetsen,
    MaatschappelijkeBaten,
    Mijlpalen,
    PeildatumEnStatus,
    TweedeKamerstukken,
)


class IndicatorlijstConfig(TypedDict):
    date_index_column: IndicatorlijstColumn | None
    data_types: dict[IndicatorlijstColumn, DataTypes]


indicatorlijst_config: dict[IndicatorlijstNamen, IndicatorlijstConfig] = {
    IndicatorlijstNamen.DOORLOOPTIJD_EN_KOSTEN: {
        "date_index_column": DoorlooptijdEnKosten.DATUM,
        "data_types": {
            DoorlooptijdEnKosten.DATUM: DataTypes.DATE,
            DoorlooptijdEnKosten.ACTUEEL_TOTAAL_PROJECTKOSTEN_OUD: DataTypes.FLOAT,
            DoorlooptijdEnKosten.ACTUEEL_TOTAAL_PROJECTKOSTEN_NIEUW: DataTypes.FLOAT,
            DoorlooptijdEnKosten.ACTUEEL_TOTAAL_PROJECTKOSTEN_CORRECT: DataTypes.FLOAT,
            DoorlooptijdEnKosten.ACTUEEL_GESCHATTE_EINDDATUM: DataTypes.DATE,
            DoorlooptijdEnKosten.ACTUEEL_HARDWARE: DataTypes.FLOAT,
            DoorlooptijdEnKosten.ACTUEEL_HARDWARE_SOFTWARE: DataTypes.FLOAT,
            DoorlooptijdEnKosten.ACTUEEL_INBESTEED_WERK: DataTypes.FLOAT,
            DoorlooptijdEnKosten.ACTUEEL_OVERIGE_PROJECTKOSTEN: DataTypes.FLOAT,
            DoorlooptijdEnKosten.ACTUEEL_STANDAARDSOFTWARE: DataTypes.FLOAT,
            DoorlooptijdEnKosten.ACTUEEL_UITBESTEED_WERK: DataTypes.FLOAT,
            DoorlooptijdEnKosten.ACTUEEL_INTERN_PERSONEEL_OUD: DataTypes.FLOAT,
            DoorlooptijdEnKosten.ACTUEEL_INTERN_PERSONEEL_NIEUW: DataTypes.FLOAT,
            DoorlooptijdEnKosten.ACTUEEL_EXTERN_PERSONEEL_OUD: DataTypes.FLOAT,
            DoorlooptijdEnKosten.ACTUEEL_EXTERN_PERSONEEL_NIEUW: DataTypes.FLOAT,
            DoorlooptijdEnKosten.ACTUEEL_DATAVERBINDINGEN: DataTypes.FLOAT,
            DoorlooptijdEnKosten.ACTUEEL_GESCHAT_OVERIG_MATERIEEL_NIEUW: DataTypes.FLOAT,
            DoorlooptijdEnKosten.DAADWERKELIJK_HARDWARE: DataTypes.FLOAT,
            DoorlooptijdEnKosten.DAADWERKELIJK_HARDWARE_SOFTWARE: DataTypes.FLOAT,
            DoorlooptijdEnKosten.DAADWERKELIJK_INBESTEED_WERK: DataTypes.FLOAT,
            DoorlooptijdEnKosten.DAADWERKELIJK_OVERIGE_PROJECTKOSTEN: DataTypes.FLOAT,
            DoorlooptijdEnKosten.DAADWERKELIJK_STANDAARDSOFTWARE: DataTypes.FLOAT,
            DoorlooptijdEnKosten.DAADWERKELIJK_UITBESTEED_WERK: DataTypes.FLOAT,
            DoorlooptijdEnKosten.DAADWERKELIJK_TOTAAL_PROJECTKOSTEN: DataTypes.FLOAT,
            DoorlooptijdEnKosten.DAADWERKELIJK_TOTAAL_PROJECTKOSTEN_NIEUW: DataTypes.FLOAT,
            DoorlooptijdEnKosten.DAADWERKELIJK_INTERN_PERSONEEL_NIEUW: DataTypes.FLOAT,
            DoorlooptijdEnKosten.DAADWERKELIJK_INTERN_PERSONEEL_OUD: DataTypes.FLOAT,
            DoorlooptijdEnKosten.DAADWERKELIJK_EXTERN_PERSONEEL_NIEUW: DataTypes.FLOAT,
            DoorlooptijdEnKosten.DAADWERKELIJK_EXTERN_PERSONEEL_OUD: DataTypes.FLOAT,
            DoorlooptijdEnKosten.DAADWERKELIJK_DATAVERBINDINGEN: DataTypes.FLOAT,
            DoorlooptijdEnKosten.DAADWERKELIJK_OVERIG_MATERIEEL_NIEUW: DataTypes.FLOAT,
            DoorlooptijdEnKosten.ACTUEEL_INTERN_PERSONEEL_CORRECT: DataTypes.FLOAT,
            DoorlooptijdEnKosten.ACTUEEL_EXTERN_PERSONEEL_CORRECT: DataTypes.FLOAT,
            DoorlooptijdEnKosten.ACTUEEL_TOTAAL_PROJECTKOSTEN_CORRECT: DataTypes.FLOAT,
            DoorlooptijdEnKosten.ACTUEEL_GESCHAT_OVERIG_MATERIEEL_CORRECT: DataTypes.FLOAT,
            DoorlooptijdEnKosten.DAADWERKELIJK_EXTERN_PERSONEEL_CORRECT: DataTypes.FLOAT,
            DoorlooptijdEnKosten.DAADWERKELIJK_OVERIG_MATERIEEL_CORRECT: DataTypes.FLOAT,
            DoorlooptijdEnKosten.DAADWERKELIJK_TOTAAL_PROJECTKOSTEN_CORRECT: DataTypes.FLOAT,
            DoorlooptijdEnKosten.DAADWERKELIJK_INTERN_PERSONEEL_CORRECT: DataTypes.FLOAT,
        },
    },
    IndicatorlijstNamen.PEILDATUM_EN_STATUS: {
        "date_index_column": None,
        "data_types": {PeildatumEnStatus.PEILDATUM: DataTypes.DATE},
    },
    IndicatorlijstNamen.MIJLPALEN: {
        "date_index_column": Mijlpalen.GEREALISEERDE_DATUM,
        "data_types": {
            Mijlpalen.GEREALISEERDE_DATUM: DataTypes.DATE,
            Mijlpalen.VERWACHTE_DATUM: DataTypes.DATE,
        },
    },
    IndicatorlijstNamen.KWALITEITSTOETSEN: {
        "date_index_column": Kwaliteitstoetsen.TOETSDATUM,
        "data_types": {Kwaliteitstoetsen.TOETSDATUM: DataTypes.DATE},
    },
    IndicatorlijstNamen.TWEEDE_KAMERSTUKKEN: {
        "date_index_column": TweedeKamerstukken.BRIEFDATUM,
        "data_types": {TweedeKamerstukken.BRIEFDATUM: DataTypes.DATE},
    },
    IndicatorlijstNamen.MAATSCHAPPELIJKE_BATEN: {
        "date_index_column": None,
        "data_types": {
            MaatschappelijkeBaten.KWANTITAIEF_JAAR: DataTypes.FLOAT,
            MaatschappelijkeBaten.KWANTITATIEF_INCIDENTEEL: DataTypes.FLOAT,
        },
    },
}


attributes_with_multiple_values = [
    ActiviteitMetrics.ONDERWERP,
    ActiviteitMetrics.DIENSTVERLENING,
    ActiviteitMetrics.BAAT,
]
