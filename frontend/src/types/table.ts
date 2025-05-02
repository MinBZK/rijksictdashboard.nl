import type { ProjectAttributePrimitiveDataType } from "@/types/project"

type Link = {
  label: string
  variableColumn: string
}

export type Column = {
  link?: Link
  hidden?: boolean
  dataType?: ProjectAttributePrimitiveDataType
}

export type TableConfig<T> = {
  key: keyof T
  link?: Link
  hidden?: boolean
  dataType?: ProjectAttributePrimitiveDataType
  label?: string
  formatInSlot?: boolean
}
