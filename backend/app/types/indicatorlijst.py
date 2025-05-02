from enum import Enum
from typing import TypedDict, Union


class DoorlooptijdEnKosten(str, Enum):
    ACTUEEL_DATAVERBINDINGEN = "Actueel dataverbindingen"
    ACTUEEL_EXTERN_PERSONEEL_OUD = "Actueel extern personeel"
    ACTUEEL_EXTERN_PERSONEEL_NIEUW = "Actueel geschat extern personeel"
    ACTUEEL_EXTERN_PERSONEEL_CORRECT = "Actueel extern personeel (correct)"
    ACTUEEL_INTERN_PERSONEEL_OUD = "Actueel intern personeel"
    ACTUEEL_INTERN_PERSONEEL_NIEUW = "Actueel geschat intern personeel"
    ACTUEEL_INTERN_PERSONEEL_CORRECT = "Actueel intern personeel (correct)"
    DAADWERKELIJK_INTERN_PERSONEEL_NIEUW = "Daadwerkelijk intern personeel (nieuw)"
    DAADWERKELIJK_INTERN_PERSONEEL_OUD = "Daadwerkelijk intern personeel (oud)"
    DAADWERKELIJK_INTERN_PERSONEEL_CORRECT = "Daadwerkelijk intern personeel (correct)"
    DAADWERKELIJK_EXTERN_PERSONEEL_NIEUW = "Daadwerkelijk extern personeel (nieuw)"
    DAADWERKELIJK_EXTERN_PERSONEEL_OUD = "Daadwerkelijk extern personeel (oud)"
    DAADWERKELIJK_EXTERN_PERSONEEL_CORRECT = "Daadwerkelijk extern personeel (correct)"
    ACTUEEL_GESCHAT_OVERIG_MATERIEEL_NIEUW = "Actueel geschat overig materieel"
    ACTUEEL_GESCHAT_OVERIG_MATERIEEL_CORRECT = "Actueel overig materieel (correct)"
    ACTUEEL_TOTAAL_PROJECTKOSTEN_NIEUW = "Actueel geschat totale projectkosten"
    ACTUEEL_GESCHATTE_EINDDATUM = "Actueel geschatte einddatum"
    ACTUEEL_HARDWARE = "Actueel hardware"
    ACTUEEL_HARDWARE_SOFTWARE = "Actueel hardware software"
    ACTUEEL_INBESTEED_WERK = "Actueel inbesteed werk"
    ACTUEEL_OVERIGE_PROJECTKOSTEN = "Actueel overige projectkosten"
    ACTUEEL_STANDAARDSOFTWARE = "Actueel standaardsoftware"
    ACTUEEL_TOTAAL_PROJECTKOSTEN_OUD = "Actueel totaal projectkosten"
    ACTUEEL_TOTAAL_PROJECTKOSTEN_CORRECT = "Actueel totaal projectkosten (correct)"
    DAADWERKELIJK_OVERIG_MATERIEEL_NIEUW = "Daadwerkelijk overig materieel"
    DAADWERKELIJK_OVERIG_MATERIEEL_CORRECT = "Daadwerkelijk overig materieel (correct)"
    ACTUEEL_UITBESTEED_WERK = "Actueel uitbesteed werk"
    DAADWERKELIJK_DATAVERBINDINGEN = "Daadwerkelijk dataverbindingen"
    DAADWERKELIJK_HARDWARE = "Daadwerkelijk hardware"
    DAADWERKELIJK_HARDWARE_SOFTWARE = "Daadwerkelijk hardware software"
    DAADWERKELIJK_INBESTEED_WERK = "Daadwerkelijk inbesteed werk"
    DAADWERKELIJK_OVERIGE_PROJECTKOSTEN = "Daadwerkelijk overige projectkosten"
    DAADWERKELIJK_STANDAARDSOFTWARE = "Daadwerkelijk standaardsoftware"
    DAADWERKELIJK_TOTAAL_PROJECTKOSTEN = "Daadwerkelijk totaal projectkosten"
    DAADWERKELIJK_TOTAAL_PROJECTKOSTEN_NIEUW = "Daadwerkelijk totale projectkosten"
    DAADWERKELIJK_TOTAAL_PROJECTKOSTEN_CORRECT = (
        "Daadwerkelijk totale projectenkosten (correct)"
    )
    DAADWERKELIJK_UITBESTEED_WERK = "Daadwerkelijk uitbesteed werk"
    DATUM = "Datum"
    KOSTEN_IN_MILJOENEN = "Kosten in miljoenen"
    PROJECTKOSTEN_IN_MILJOENEN = "Projectkosten in miljoenen"
    REDEN_HERIJKING = "Reden herijking"
    SOORT_ACTIE = "Soort actie"
    TOELICHTING_WIJZIGING_EINDDATUM = "Toelichting wijziging einddatum"
    TOELICHTING_WIJZIGING_KOSTEN = "Toelichting wijziging kosten"


class Ontwikkelpartijen(str, Enum):
    ONTWIKKELPARTIJ = "Ontwikkelpartij"
    ROL = "Rol"


class Mijlpalen(str, Enum):
    KWANTITATIEF_INCIDENTEEL = "Kwantitatief incidenteel"
    VERWACHTE_DATUM = "Verwachte datum"
    KWANTITATIEF_JAAR = "Kwantitatief jaar"
    CONFORM_EISEN = "Conform eisen"
    GEREALISEERDE_DATUM = "Gerealiseerde datum"
    PROJECTPLANVERSIE = "Projectplanversie"
    MIJLPAAL_BEHAALD = "Mijlpaal behaald"
    MIJLPAAL_OMSCHRIJVING = "Mijlpaal omschrijving"


class Kwaliteitstoetsen(str, Enum):
    TOETSDATUM = "Toetsdatum"
    UITVOERENDE_PARTIJ = "Uitvoerende partij"
    SOORT_TOETS = "Soort toets"
    OMSCHRIJVING = "Omschrijving"


class TweedeKamerstukken(str, Enum):
    LINK = "Link"
    TITEL = "Titel"
    NUMMER = "Nummer"
    ACICT_ADVIES = "AcICT-advies"
    BRIEFDATUM = "Briefdatum"


class MaatschappelijkeBaten(str, Enum):
    TOELICHTING = "Toelichting"
    KWANTITATIEF_INCIDENTEEL = "Kwantitatief incidenteel"
    KWANTITAIEF_JAAR = "Kwantitatief jaar"


class PeildatumEnStatus(str, Enum):
    PEILDATUM = "Peildatum"
    STATUS = "Status"


class IndicatorlijstFilter(TypedDict):
    indicatortitel: Union[
        PeildatumEnStatus,
        MaatschappelijkeBaten,
        TweedeKamerstukken,
        Kwaliteitstoetsen,
        Mijlpalen,
        Ontwikkelpartijen,
        DoorlooptijdEnKosten,
    ]
    waarde: str
