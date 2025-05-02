import type {
  IndicatorLijst,
  ProjectMetAlleMetricsEnIndicatorLijsten,
  Metrics,
  Project,
} from "@/api-new"

export type ProjectAttribute = keyof ProjectMetAlleMetricsEnIndicatorLijsten

export type ProjectResponse = {
  results: Project[]
  total_count: number
  aggregations: ProjectAggregation[]
  ministeries: string[]
  metrics: Metrics
}

export interface ProjectMetAttributen extends Project {
  IndicatorLijstWaardes: IndicatorLijst[]
}

export type ProjectNumber = {
  afkorting: string
  omschrijving: string
  aantal: number
}

export type ProjectAttributePrimitiveDataType =
  | "string"
  | "currency"
  | "list"
  | "number"
  | "date"
  | "integer"
  | "currency-million"
  | "number-double-digit"
  | "percentage"

export type ProjectAttributePrimitive = {
  key: string
  label: string
  dataType: ProjectAttributePrimitiveDataType
}

export type AttributeAggregation = {
  aggregation_value: string
  count: number
}

export type ProjectAggregation = {
  aggregation_attribute: ProjectAttribute
  values: AttributeAggregation[]
}

export type ProjectFilter = {
  attribute: ProjectAttribute
  values: string[]
}

export type AttributeSorting = {
  attribute: ProjectAttribute
  direction: "asc" | "desc"
}

export type ProjectStatus =
  | "In heroriëntatie"
  | "In uitvoering"
  | "Geannuleerd"
  | "Afgerond"
  | "Nog niet gestart"

export type List =
  | "Top 3 recent toegevoegde ICT-activiteiten"
  | "Top 3 recent afgeronde ICT-activiteiten"

export type ListConfig<T> = {
  listName: List
  label: string
  caption: string
  attributes: Array<{
    item: keyof T
    type: "string" | "date"
  }>
}
