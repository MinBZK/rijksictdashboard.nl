import type { IndicatorlijstNamen } from "@/api-new"
import type { ProjectAttribute } from "@/types/project"

export type IndicatorLijstConfig = {
  urlFields?: string[]
  hiddenFields?: string[]
}

type GeneralConfig = {
  indicatorLijstEnkel: string[]
  kostenSeriesIndicatoren: any
  indicatorTitelDatumDoorlooptijdEnKosten: string
}

export type IndicatorLijstenConfig = Partial<
  Record<IndicatorlijstNamen, IndicatorLijstConfig>
>

type CmsConfig = {
  general: GeneralConfig
  indicatorLijsten: IndicatorLijstenConfig
  attributeConfig: Partial<Record<ProjectAttribute, AttributeConfig>>
}

type AttributeConfig = {
  pluralLabel: string
  routerName: string
  displayLabel: string
}

const cmsConfig: CmsConfig = {
  general: {
    indicatorLijstEnkel: ["Algemeen"],
    indicatorTitelDatumDoorlooptijdEnKosten: "Datum",
    kostenSeriesIndicatoren: {
      "Actueel totaal projectkosten (correct)": "Geschatte meerjarige uitgaven",
      "Daadwerkelijk totale projectenkosten (correct)":
        "Gerealiseerde meerjarige uitgaven",
    },
  },
  indicatorLijsten: {
    "Tweede Kamerstukken": {
      urlFields: ["Link"],
      hiddenFields: ["AcICT-advies"],
    },
    "Doorlooptijd en Kosten": {
      hiddenFields: [
        "Actueel hardware",
        "Actueel hardware software",
        "Actueel inbesteed werk",
        "Actueel intern personeel",
        "Actueel overige projectkosten",
        "Actueel standaardsofware",
        "Actueel dataverbindingen",
        "Actueel extern personeel",
        "Actueel totaal projectkosten",
        "Actueel uitbesteed werk",
        "Actueel standaardsoftware",
        "Actueel geschat totale projectkosten",
        "Actueel geschat intern personeel",
        "Actueel geschat extern personeel",
        "Actueel geschat overig materieel",
        "Daadwerkelijk totale projectkosten",
        "Daadwerkelijk dataverbindingen",
        "Daadwerkelijk hardware",
        "Daadwerkelijk hardware software",
        "Daadwerkelijk totaal projectkosten",
        "Daadwerkelijk uitbesteed werk",
        "Daadwerkelijk intern personeel (oud)",
        "Daadwerkelijk intern personeel (nieuw)",
        "Daadwerkelijk inbesteed werk",
        "Daadwerkelijk extern personeel (oud)",
        "Daadwerkelijk extern personeel (nieuw)",
        "Daadwerkelijk standaardsoftware",
        "Daadwerkelijk overige projectkosten",
        "Daadwerkelijk overig materieel",
        "Actueel totaal projectkosten (correct)",
        "Actueel extern personeel (correct)",
        "Daadwerkelijk extern personeel (correct)",
        "Actueel intern personeel (correct)",
        "Daadwerkelijk intern personeel (correct)",
        "Daadwerkelijk totale projectenkosten (correct)",
        "Daadwerkelijk overig materieel (correct)",
        "Actueel overig materieel (correct)",
        "Kosten in miljoenen",
        "Projectkosten in miljoenen",
        "Gefinancierd door de Europese Unie",
      ],
    },
  },
  attributeConfig: {
    MinisterieNaam: {
      pluralLabel: "ministeries",
      routerName: "ministerie",
      displayLabel: "Ministerie",
    },
    Onderwerp: {
      pluralLabel: "onderwerpen",
      routerName: "onderwerp",
      displayLabel: "Onderwerp",
    },
    Dienstverlening: {
      pluralLabel: "dienstverleningen",
      routerName: "dienstverlening",
      displayLabel: "Dienstverlening",
    },
    SoortICTActiviteit: {
      pluralLabel: "soorten activiteiten",
      routerName: "soort",
      displayLabel: "Soort ICT-activiteit",
    },
    MaatschappelijkeBaat: {
      pluralLabel: "Wij verbeteren op",
      routerName: "wat we verbeteren detail",
      displayLabel: "Verbetert op",
    },
  },
}

export default cmsConfig
