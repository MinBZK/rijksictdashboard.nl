export type CostsPerMinistry = {
  kosten: number
  afkorting: number
}

export type ProjectPerSubject = {
  Onderwerp: string
  Aantal: number
  Label?: string
}

export type ProjectAggregation = {
  attribute: string
  count: number
}

export type ProjectPerStatusPerYear = {
  Status: string
  Aantal: number
  Jaar: number
}
