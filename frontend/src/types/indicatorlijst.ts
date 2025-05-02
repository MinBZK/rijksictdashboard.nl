import type { Formulier, IndicatorLijst } from "@/api-new"

export type IndicatorLijsten = {
  Beheer?: string
  Algemeen?: string
  "Tweede Kamerstukken"?: string
  "Maatschappelijke baten"?: string
  Ontwikkelpartijen?: string
  Kwaliteitstoetsen?: string
  Mijlpalen?: string
  "Doorlooptijd en Kosten": string
}

export type IndicatorAntwoordTypeNaam =
  | "Tekst"
  | "Getal"
  | "Datum"
  | "EnkeleKeuze"
  | "MeerKeuze"
  | "Tussenkopje"
  | "EnkeleKeuzeLijst"
  | "Tekstveld"
  | "Bedrag"
  | "Tabel"
  | "Tabelcel"

export type IndicatorWaarde = {
  IndicatorTitel: string
  Waarde: string | null
  IndicatorIndex: number
  IndicatorAntwoordTypeNaam: IndicatorAntwoordTypeNaam
}

// export type IndicatorLijst = {
//   Formulier: Formulier[]
//   IndicatorLijstEnkelFormulier: boolean
//   IndicatorLijstMeervoudsNaam: IndicatorLijstNaam
//   IndicatorLijstIndex: number
//   DatumIndexVeld: string | null
// }

export interface IndicatorLijstMetBerekendeAttributen extends IndicatorLijst {
  FormulierGefilterd: Formulier[]
}
