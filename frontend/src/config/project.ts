import type { ProjectAttributePrimitive } from "@/types/project"

const columns: ProjectAttributePrimitive[] = [
  { key: "Naam", label: "Naam", dataType: "string" },
]

const columnMapping = columns.reduce((mapping, obj) => {
  //@ts-expect-error
  mapping[obj.key] = obj.label
  return mapping
}, {})

export { columns, columnMapping }
