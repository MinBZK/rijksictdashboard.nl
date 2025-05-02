import type { ProjectMetCoreMetrics } from "@/api-new"
import type { Ref } from "vue"

type ValueOf<T> = T[keyof T]
export type AttributeValueType = ValueOf<ProjectMetCoreMetrics>

export type DataFilter = {
  attribute: keyof ProjectMetCoreMetrics
  values: AttributeValueType[]
}

export function useFilteredProjecten(
  projecten: Ref<ProjectMetCoreMetrics[] | undefined>,
  filters: Ref<DataFilter[]>,
) {
  const preprocessedProjecten = computed(() => {
    return (projecten.value || []).map((p) => {
      Object.entries(p).forEach(([attr, value]) => {
        if (value === null || value == undefined || value == "") {
          //@ts-expect-error: types lost with Object.entries
          p[attr] = null
        }
      })

      return p
    })
  })

  function projectHasValue(
    project: ProjectMetCoreMetrics,
    attribute: DataFilter["attribute"],
    filterValue: AttributeValueType,
  ) {
    const projectValue = project[attribute]
    const projectValues =
      typeof projectValue === "string"
        ? projectValue.split(";")
        : [projectValue]
    return projectValues.some((v) => v === filterValue)
  }

  function filterProjecten(filters: DataFilter[]) {
    const hasFilters = filters.map((f) => f.values).flat().length > 0
    return (preprocessedProjecten.value || []).filter((project) =>
      hasFilters
        ? filters.every(({ attribute, values: filterValues }) =>
            filterValues.some((filterValue) =>
              projectHasValue(project, attribute, filterValue),
            ),
          )
        : true,
    )
  }

  const filteredProjecten = computed(() => filterProjecten(filters.value))

  function removeFilterValue(
    attribute: DataFilter["attribute"],
    filterValue: DataFilter["values"][0],
  ) {
    const chartFiltersCopy = [...filters.value]
    const chartFilter = chartFiltersCopy.find(
      (filter) => filter.attribute === attribute,
    )
    if (chartFilter) {
      chartFilter.values = chartFilter.values.filter(
        (value) => value !== filterValue,
      )
    }
    filters.value = chartFiltersCopy
  }

  const dataFiltersFlat = computed(() =>
    filters.value.flatMap((filter) => {
      return filter.values.map((value) => ({
        attribute: filter.attribute,
        filterValue: value,
      }))
    }),
  )

  return {
    projecten,
    preprocessedProjecten,
    filteredProjecten,
    filters,
    dataFiltersFlat,
    removeFilterValue,
    filterProjecten,
    projectHasValue,
  }
}
