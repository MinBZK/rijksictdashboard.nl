<script setup lang="ts">
import type { ProjectMetCoreMetrics } from "@/api-new/models/ProjectMetCoreMetrics"
import type { ItemSelect } from "@/types/components"
import cmsConfig from "@/config/cms"
import { sortArrayByKey } from "@/util"
import type {
  DataFilter,
  AttributeValueType,
} from "@/composables/useFilteredProjecten"
import { useFilteredProjecten } from "@/composables/useFilteredProjecten"

const props = defineProps<{
  filterAttributes: (keyof ProjectMetCoreMetrics)[]
  projecten: ProjectMetCoreMetrics[]
}>()

const projecten = toRef(props, "projecten")

const chartFilters = defineModel<DataFilter[]>({
  required: true,
})

const { filterProjecten, projectHasValue } = useFilteredProjecten(
  projecten,
  chartFilters,
)

const filterItem = (
  filterValue: AttributeValueType,
  count?: number,
): ItemSelect => {
  const title = filterValue || "(Niet ingevuld)"
  const result = {
    value: filterValue,
    title: title + (count !== undefined ? ` (${count})` : ""),
  }
  return result
}

function getFilterValues(attribute: keyof ProjectMetCoreMetrics): ItemSelect[] {
  // To get a list of available filters, apply all filters to the dataset except filters which are already on the current attribute.
  // If you don't remove this, you will only see the value you have selected.
  const filteredProjecten = filterProjecten(
    chartFilters.value.filter((f) => f.attribute !== attribute),
  )

  const filterValues = [
    ...new Set(
      filteredProjecten
        .map((p) => p[attribute])
        // split by semicolon for one-to-many values
        .map((fV) => (typeof fV == "string" ? fV.split(";") : fV))
        .flat(),
    ),
  ]

  return sortArrayByKey(
    filterValues.map((fV) => {
      const count = filteredProjecten.filter((p) =>
        projectHasValue(p, attribute, fV),
      ).length
      return filterItem(fV, count)
    }),
    "title",
  )
}

function uncapitalizeFirstChar(text: string) {
  return text.charAt(0).toLowerCase() + text.slice(1)
}

function updateChartFilters(
  attribute: keyof ProjectMetCoreMetrics,
  values: string[],
) {
  const existingFilter = chartFilters.value.find(
    (filter) => filter.attribute === attribute,
  )

  if (values.length == 0 && existingFilter) {
    const index = chartFilters.value.indexOf(existingFilter)
    if (index > -1) {
      chartFilters.value.splice(index, 1)
    }
  } else if (existingFilter) {
    existingFilter.values = values
  } else {
    chartFilters.value.push({ attribute, values })
  }
}

const itemLabelKey = "title"
const itemValueKey = "value"

function getModelValue(attribute: DataFilter["attribute"]) {
  const filterValues =
    chartFilters.value.find((f) => f.attribute === attribute)?.values || []
  return filterValues.map((v) => {
    return filterItem(v)
  })
}
</script>

<template>
  <v-col v-for="attr in filterAttributes" :key="attr" :lg="3" class="mt-4">
    <DropdownSelectMultiple
      :items="getFilterValues(attr)"
      :label="`Filter op ${uncapitalizeFirstChar(cmsConfig.attributeConfig[attr]?.displayLabel || '')}`"
      :item-label-key="itemLabelKey"
      :item-value-key="itemValueKey"
      :model-value="getModelValue(attr)"
      @update:model-value="
        (selectedValues) =>
          updateChartFilters(
            attr,
            selectedValues.map((v: Record<string, any>) => v['value']),
          )
      "
    />
  </v-col>
</template>
