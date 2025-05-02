from enum import Enum

from .indicatorlijst import (
    DoorlooptijdEnKosten,
    IndicatorlijstFilter,
    Kwaliteitstoetsen,
    MaatschappelijkeBaten,
    Mijlpalen,
    Ontwikkelpartijen,
    PeildatumEnStatus,
    TweedeKamerstukken,
)
from .jbr_activiteiten_overzicht import ActiviteitMetrics
from .project import ProjectAttributeSorting, ProjectFilter
from .search import ComparisonType

__all__ = [
    "Publicatiestatus",
    "IndicatorlijstNamen",
    "DataTypes",
    "DoorlooptijdEnKosten",
    "Ontwikkelpartijen",
    "Mijlpalen",
    "Kwaliteitstoetsen",
    "TweedeKamerstukken",
    "MaatschappelijkeBaten",
    "ActiviteitMetrics",
    "PeildatumEnStatus",
    "Publicatiestatus",
    "Projectstatus",
    "IndicatorlijstFilter",
    "ProjectFilter",
    "ProjectAttributeSorting",
    "ComparisonType",
]


IndicatorlijstColumn = (
    DoorlooptijdEnKosten
    | TweedeKamerstukken
    | Kwaliteitstoetsen
    | Mijlpalen
    | PeildatumEnStatus
    | MaatschappelijkeBaten
)


class Publicatiestatus(str, Enum):
    GEEN = "Geen"
    GEPUBLICEERD = "Gepubliceerd"
    GECONTROLEERD = "Gecontroleerd"
    CONCEPT = "Concept"


class Projectstatus(str, Enum):
    AFGEROND = "Afgerond"
    GEANNULEERD = "Geannuleerd"
    IN_HERORIENTATIE = "In heroriëntatie"
    IN_UITVOERING = "In uitvoering"
    NOG_NIET_GESTART = "Nog niet gestart"


class IndicatorlijstNamen(str, Enum):
    DOORLOOPTIJD_EN_KOSTEN = "Doorlooptijd en Kosten"
    ONTWIKKELPARTIJEN = "Ontwikkelpartijen"
    KWALITEITSTOETSEN = "Kwaliteitstoetsen"
    MIJLPALEN = "Mijlpalen"
    MAATSCHAPPELIJKE_BATEN = "Maatschappelijke baten"
    BEHEER = "Beheer"
    TWEEDE_KAMERSTUKKEN = "Tweede Kamerstukken"
    PEILDATUM_EN_STATUS = "Peildatum en Status"
    ALGEMEEN = "Algemeen"


class DataTypes(str, Enum):
    DATE = "date"
    FLOAT = "float"
    STRING = "string"
