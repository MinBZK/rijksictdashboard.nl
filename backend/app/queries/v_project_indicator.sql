select
    p."Naam" as "Naam",
    pv."Id" as "ProjectVersieId",
    i."Id" as "IndicatorId",
    il."Id" as "IndicatorLijstId",
    pv."ProjectId" as "ProjectId",
    a."Id" as "AntwoordId",    
    f."Id" as "FormulierId",
    pv."Versie" as "ProjectVersie",
    pvst."Naam" as "ProjectVersieStatusNaam",
    pvst."Id" as "ProjectVersieStatusId",
    il."MeervoudsNaam" as "IndicatorLijstMeervoudsNaam",
    il."EnkelFormulier" as "IndicatorLijstEnkelFormulier",
    f."AanmaakDatum" as "FormulierAanmaakDatum",
    i."Titel" as "IndicatorTitel",
    a."Waarde" as "Waarde",
    pv."WijzigingsDatum" as "WijzigingsDatum",
    m."Naam" as "MinisterieNaam"
from
    "ProjectVersie" pv
    join "FormulierProjectVersie" fpv on fpv."ProjectVersiesId" = pv."Id"
    join "Formulier" f on f."Id" = fpv."FormulierenId"
    join "Antwoord" a on a."FormulierId" = f."Id"
    join "Indicator" i on i."Id" = a."IndicatorId"
    join "IndicatorLijst" il on il."Id" = i."IndicatorLijstId"
    join "Project" p on p."Id" = pv."ProjectId"
    join "ProjectVersieStatus" pvst on pvst."Id" = pv."StatusId"
    Join "Ministerie" m on m."Id" = p."MinisterieId"