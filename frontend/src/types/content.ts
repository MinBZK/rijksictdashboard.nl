export type ContentMinisterie = {
  Ministerie: Ministeries
}

export type Bewindspersoon = {
  naam: string
  portretBron: string
}

export type Ministerie = {
  omschrijving: string[]
  minister: Bewindspersoon[]
  staatssecretaris?: Bewindspersoon[]
  url: string
  img: string
  imgAuthor?: string
  altText?: string
  iplanKey?: string
  hideIplan?: boolean
}

export type Ministeries = {
  "Algemene Zaken": Ministerie
  "Asiel en Migratie": Ministerie
  "Binnenlandse Zaken en Koninkrijksrelaties": Ministerie
  "Buitenlandse Zaken": Ministerie
  Defensie: Ministerie
  "Economische Zaken": Ministerie
  Financiën: Ministerie
  "Infrastructuur en Waterstaat": Ministerie
  "Klimaat en Groene Groei": Ministerie
  "Justitie en Veiligheid": Ministerie
  "Landbouw, Visserij, Voedselzekerheid en Natuur": Ministerie
  "Onderwijs, Cultuur en Wetenschap": Ministerie
  "Sociale Zaken en Werkgelegenheid": Ministerie
  "Volksgezondheid, Welzijn en Sport": Ministerie
  "Volkshuisvesting en Ruimtelijke Ordening": Ministerie
}

type Subonderwerp = {
  subonderwerp: string
  waarde: string
}

export type Onderwerp = {
  img?: string
  imgAuthor?: string
  subonderwerpen: Subonderwerp[]
  urlRijksoverheid: string
}

export type OnderwerpenKey =
  | "Belastingen, uitkeringen en toeslagen"
  | "Recht, veiligheid en defensie"
  | "Belastingen, uitkeringen en toeslagen"
  | "Recht, veiligheid en defensie"
  | "Bouwen en wonen"
  | "Economie"
  | "Familie, zorg en gezondheid"
  | "Internationale samenwerking"
  | "Klimaat, milieu en natuur"
  | "Migratie en reizen"
  | "Onderwijs"
  | "Overheid en democratie"
  | "Verkeer en vervoer"
  | "Werk"

export type Onderwerpen = Record<OnderwerpenKey, Onderwerp>

export type RapportageGeschiedenis = {
  jaar: number
  nummer?: string
  omschrijving: string
  link: string
}
