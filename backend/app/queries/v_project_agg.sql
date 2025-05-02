with ProjectVersieAttributen as (
  select
    pv."Id" as "ProjectVersieId",
    pv."ProjectId" as "ProjectId",
    il."Id" as "IndicatorLijstId",
    il."MeervoudsNaam" as "IndicatorLijstMeervoudsNaam",
    il."EnkelFormulier" as "IndicatorLijstEnkelFormulier",
    il."Index" as "IndicatorLijstIndex",
    f."Id" as "FormulierId",
    f."AanmaakDatum" as "FormulierAanmaakDatum",
    i."Titel" as "IndicatorTitel",
    i."Index" as "IndicatorIndex",
    awty."Naam" as "IndicatorAntwoordTypeNaam",
    a."Waarde" as "Waarde",
    case
      when il."MeervoudsNaam" = 'Doorlooptijd en Kosten'
      and (
        i."Titel" = 'Daadwerkelijk extern personeel'
        or i."Titel" = 'Daadwerkelijk intern personeel'
      )
      and i."Index" = 7 then concat(i."Titel", ' (oud)')
      when il."MeervoudsNaam" = 'Doorlooptijd en Kosten'
      and (
        i."Titel" = 'Daadwerkelijk extern personeel'
        or i."Titel" = 'Daadwerkelijk intern personeel'
      )
      and i."Index" = 6 then concat(i."Titel", ' (nieuw)')
      else i."Titel"
    end as "IndicatorTitelGecorrigeerd"
  from
    "ProjectVersie" pv
    left join "FormulierProjectVersie" fpv on fpv."ProjectVersiesId" = pv."Id"
    left join "Formulier" f on f."Id" = fpv."FormulierenId"
    left join "Antwoord" a on a."FormulierId" = f."Id"
    left join "Indicator" i on i."Id" = a."IndicatorId"
    left join "IndicatorLijst" il on il."Id" = i."IndicatorLijstId"
    left join "AntwoordType" awty on awty."Id" = i."AntwoordTypeId"
),
ProjectVersieAttributenAgg as (
  select
    "ProjectVersieId",
    "ProjectId",
    "FormulierId",
    "FormulierAanmaakDatum",
    "IndicatorLijstId",
    "IndicatorLijstMeervoudsNaam",
    "IndicatorLijstEnkelFormulier",
    "IndicatorLijstIndex",
    json_agg(
      json_build_object(
        'IndicatorTitel',
        "IndicatorTitelGecorrigeerd",
        'IndicatorIndex',
        "IndicatorIndex",
        'Waarde',
        "Waarde",
        'IndicatorAntwoordTypeNaam',
        "IndicatorAntwoordTypeNaam"
      )
    ) as "FormulierWaardes"
  from
    ProjectVersieAttributen
  group by
    "ProjectId",
    "ProjectVersieId",
    "FormulierId",
    "FormulierAanmaakDatum",
    "IndicatorLijstId",
    "IndicatorLijstMeervoudsNaam",
    "IndicatorLijstEnkelFormulier",
    "IndicatorLijstIndex"
),
ProjectVersieIndicatorLijstAgg as (
  select
    "ProjectVersieId",
    "ProjectId",
    "IndicatorLijstId",
    "IndicatorLijstMeervoudsNaam",
    "IndicatorLijstEnkelFormulier",
    "IndicatorLijstIndex",
    coalesce(
      json_agg(
        json_build_object(
          'FormulierId',
          "FormulierId",
          'FormulierAanmaakDatum',
          "FormulierAanmaakDatum",
          'FormulierWaardes',
          "FormulierWaardes"
        )
      ) filter (
        WHERE
          "FormulierId" is not null
      ),
      '[]'
    ) as "Formulier"
  from
    ProjectVersieAttributenAgg
  group by
    "ProjectVersieId",
    "ProjectId",
    "IndicatorLijstId",
    "IndicatorLijstMeervoudsNaam",
    "IndicatorLijstEnkelFormulier",
    "IndicatorLijstIndex"
),
ProjectVersieAgg as (
  select
    "ProjectVersieId",
    "ProjectId",
    coalesce(
      json_agg(
        json_build_object(
          'IndicatorLijstId',
          "IndicatorLijstId",
          'IndicatorLijstMeervoudsNaam',
          "IndicatorLijstMeervoudsNaam",
          'IndicatorLijstEnkelFormulier',
          "IndicatorLijstEnkelFormulier",
          'IndicatorLijstIndex',
          "IndicatorLijstIndex",
          'Formulier',
          "Formulier"
        )
      ) filter (
        where
          "IndicatorLijstId" is not null
      ),
      '[]'
    ) as "IndicatorLijstWaardes",
    coalesce(
      array_agg("IndicatorLijstMeervoudsNaam") filter (
        WHERE
          "IndicatorLijstMeervoudsNaam" is not null
      ),
      '{}'
    ) as "IndicatorLijstBeschikbaar"
  from
    ProjectVersieIndicatorLijstAgg
  group by
    "ProjectVersieId",
    "ProjectId"
),
ProjectVersieSamenvatting as (
  select
    "ProjectVersieId",
    json_object_agg("IndicatorTitel", "Waarde") as "ProjectSamenvatting"
  from
    ProjectVersieAttributen
  where
    "IndicatorLijstMeervoudsNaam" in ('Algemeen', 'Peildatum en Status')
  group by
    "ProjectVersieId"
)
select
  p.*,
  pvs."ProjectSamenvatting" as "Samenvatting",
  pv."Versie" as "ProjectVersie",
  pvst."Naam" as "ProjectVersieStatusNaam",
  pvst."Id" as "ProjectVersieStatusId",
  pvAgg.*,
  trim(
    '"'
    from
      cast(pvs."ProjectSamenvatting" -> 'Onderwerp' as text)
  ) as "Onderwerp",
  trim(
    '"'
    from
      cast(pvs."ProjectSamenvatting" -> 'Status' as text)
  ) as "ProjectStatus",
  trim(
    '"'
    from
      cast(
        pvs."ProjectSamenvatting" -> 'Startdatum' as text
      )
  ) as "StartDatum",
  to_date(
    trim(
      '"'
      from
        cast(pvs."ProjectSamenvatting" -> 'Peildatum' as text)
    ),
    'YYYY-MM-DD'
  ) as "PeilDatum",
  extract(
    year
    from
      to_date(
        trim(
          '"'
          from
            cast(pvs."ProjectSamenvatting" -> 'Peildatum' as text)
        ),
        'YYYY-MM-DD'
      )
  ) as "PeilDatumJaar",
  pv."WijzigingsDatum" as "ProjectVersieWijzigingsDatum",
  m."Naam" as "MinisterieNaam",
  m."Afkorting" as "MinisterieAfkorting",
  o."Naam" as "OrganisatieNaam"
from
  ProjectVersieAgg pvAgg
  join "Project" p on p."Id" = pvAgg."ProjectId"
  left join ProjectVersieSamenvatting pvs on pvs."ProjectVersieId" = pvAgg."ProjectVersieId"
  join "ProjectVersie" pv on pv."Id" = pvAgg."ProjectVersieId"
  join "Ministerie" m on m."Id" = p."MinisterieId"
  join "ProjectVersieStatus" pvst on pvst."Id" = pv."StatusId"
  left join "Organisatie" o on o."Id" = p."OrganisatieId"