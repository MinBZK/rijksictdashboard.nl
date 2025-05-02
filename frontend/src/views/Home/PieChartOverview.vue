<template>
  <RidChart
    :chart-data="chartData"
    :chart-type="'pieChart'"
    :label-horizontal="chartConfig.xAttribute"
    :label-horizontal-table="chartConfig.xAttributeDisplayLabel"
    :label-measure="selectedAggregation"
    x-data-type="string"
    :y-data-type="
      selectedAggregation == 'Kosten' ? 'currency-million' : 'integer'
    "
    :y-axis-integer="true"
    :caption="'caption'"
    :title="chartTitle"
  >
    <template #chart-top="{ showTable }">
      <v-row>
        <v-col :lg="3">
          <Dropdown
            v-model="groupByAttribute"
            :items="groupByOptions || []"
            label="Vergelijken per"
          />
        </v-col>
        <ChartFilters
          v-model="dataFilters"
          :filter-attributes="filterAttributes"
          :projecten="preprocessedProjecten"
        />
      </v-row>
      <ButtonToggle
        v-model="selectedAggregation"
        :options="chartAggregationLabels"
        class="my-4"
      />

      <h3 v-if="!showTable" class="text-center">
        {{ chartTitle }}
      </h3>

      <v-chip
        v-for="{ attribute, filterValue } in dataFiltersFlat"
        :key="attribute + (filterValue ? filterValue.toString() : '')"
        class="mr-3 mb-3"
        :color="getAttributeColor(attribute)"
        :aria-label="`Verwijder filter ${attribute} = ${filterValue || '(Niet ingevuld)'}`"
        closable
        size="large"
        role="button"
        tabindex="0"
        @keyup.enter="removeFilterValue(attribute, filterValue)"
        @click="removeFilterValue(attribute, filterValue)"
      >
        {{ cmsConfig.attributeConfig[attribute]?.displayLabel }}:
        {{ filterValue || "(niet ingevuld)" }}</v-chip
      >
    </template>
  </RidChart>
  <ExpandContent
    :title="`Bijbehorende ICT-activiteiten (${filteredProjecten.length})`"
    title-level="h3"
    :auto-expand="false"
  >
    <TableOverview :projecten="filteredProjecten" :rows-per-page="5" />
  </ExpandContent>
</template>

<script setup lang="ts">
import type { ProjectMetCoreMetrics } from "@/api-new/models/ProjectMetCoreMetrics"
import { useMetrics } from "@/composables/useMetrics"
import type { DataFilter } from "@/composables/useFilteredProjecten"
import { useFilteredProjecten } from "@/composables/useFilteredProjecten"
import type { LineChartDatapoint } from "@/types/chart"
import cmsConfig from "@/config/cms"
import type { ItemSelect } from "@/types/components"
import type { Colors } from "@/types/colors"

const { projectenMetMetrics } = useMetrics({
  statusType: "all",
  autoLoad: true,
})

const projecten = computed(() => projectenMetMetrics.value?.results)
const dataFilters = ref<DataFilter[]>([])

const {
  filteredProjecten,
  removeFilterValue,
  dataFiltersFlat,
  preprocessedProjecten,
} = useFilteredProjecten(projecten, dataFilters)

type Aggregation = {
  method: "count" | "sum"
  aggregationAttribute?: keyof ProjectMetCoreMetrics
}

type ChartConfig = {
  xAttribute: keyof ProjectMetCoreMetrics
  xAttributeDisplayLabel: string
  aggregation: Aggregation
}

type GroupByFilter = {
  attribute: keyof ProjectMetCoreMetrics
  filterValue: string | number | null
}

type AggregationLabel = "Aantal ICT-activiteiten" | "Kosten"
const chartAggregationLabels: AggregationLabel[] = [
  "Aantal ICT-activiteiten",
  "Kosten",
]
const selectedAggregation = ref(chartAggregationLabels[0])
const groupByAttribute = ref<keyof ProjectMetCoreMetrics>("SoortICTActiviteit")

const chartConfig = computed((): ChartConfig => {
  const xAttribute = groupByAttribute.value
  const xAttributeDisplayLabel =
    cmsConfig.attributeConfig[xAttribute]?.displayLabel

  if (!xAttributeDisplayLabel)
    throw new Error(`Display label not defined for ${xAttribute} in cmsConfig`)

  return {
    xAttribute,
    xAttributeDisplayLabel,
    aggregation: {
      method:
        selectedAggregation.value == "Aantal ICT-activiteiten"
          ? "count"
          : "sum",
      aggregationAttribute:
        selectedAggregation.value == "Aantal ICT-activiteiten"
          ? undefined
          : "SchattingTotaleKostenHuidigJaar",
    },
  }
})

function aggregateProjecten(
  projecten: ProjectMetCoreMetrics[],
  filter: GroupByFilter,
  aggregation: Aggregation,
) {
  const aggregatedValues = projecten
    .filter((p) => p[filter.attribute] == filter.filterValue)
    .map((p) => p[aggregation.aggregationAttribute || "ActiviteitId"])
  if (aggregation.method === "count") {
    return aggregatedValues.length
  } else if (aggregation.method === "sum") {
    const parsedValues = aggregatedValues.map(
      (v) => parseFloat(v as string) || 0,
    )
    return parsedValues.reduce((acc, value) => acc + value, 0)
  } else {
    return 0
  }
}

const chartData = computed((): LineChartDatapoint[] => {
  const categoryAttribute = chartConfig.value.xAttribute
  const projecten = filteredProjecten.value

  const splittedValues = projecten
    .map((project) => {
      const value = project[categoryAttribute]
      if (typeof value == "string") {
        return value.split(";")
      } else {
        return value
      }
    })
    .flat()
  const uniqueCategories = [...new Set(splittedValues)].sort()

  return uniqueCategories.map((category): LineChartDatapoint => {
    return {
      x:
        typeof category == "number"
          ? category.toString()
          : category || `${chartConfig.value.xAttributeDisplayLabel} onbekend`,
      y: aggregateProjecten(
        projecten,
        {
          attribute: categoryAttribute,
          filterValue: category,
        },
        chartConfig.value.aggregation,
      ),
      label: selectedAggregation.value,
    }
  })
})

function uncapitalizeFirstChar(text: string) {
  return text.charAt(0).toLowerCase() + text.slice(1)
}

const chartTitle = computed(() => {
  const displayLabel =
    cmsConfig.attributeConfig[chartConfig.value.xAttribute]?.displayLabel
  if (!displayLabel)
    throw new Error(
      `Display label not defined for ${chartConfig.value.xAttribute}`,
    )
  return `${selectedAggregation.value} per ${uncapitalizeFirstChar(displayLabel)}`
})

const groupByOptions = computed((): ItemSelect[] => {
  const groupByAttributes: (keyof ProjectMetCoreMetrics)[] = [
    "SoortICTActiviteit",
    "MinisterieNaam",
  ]

  return groupByAttributes.map((attribute) => {
    const displayLabel = cmsConfig.attributeConfig[attribute]?.displayLabel
    if (!displayLabel)
      throw new Error(`Display label not defined for ${attribute}`)
    return {
      title: displayLabel,
      value: attribute,
    }
  })
})

const filterAttributes = computed(() => {
  const allFilterAttributes: (keyof ProjectMetCoreMetrics)[] = [
    "SoortICTActiviteit",
    "MinisterieNaam",
    "Onderwerp",
  ]

  return allFilterAttributes.filter(
    (attribute) => attribute !== groupByAttribute.value,
  )
})

type AttributeConfig = {
  color: Colors
}
type AttributeConfigDict = Partial<
  Record<keyof ProjectMetCoreMetrics, AttributeConfig>
>

const attributeConfig: AttributeConfigDict = {
  SoortICTActiviteit: {
    color: "hemelblauw",
  },
  MinisterieNaam: {
    color: "groen",
  },
  Onderwerp: {
    color: "oranje",
  },
}

function getAttributeColor(attribute: keyof ProjectMetCoreMetrics) {
  return attributeConfig[attribute]?.color || "grijs7"
}

watch(groupByAttribute, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    dataFilters.value = []
  }
})
</script>

<style scoped lang="scss">
@import "@/styles/_colors.scss";

.v-btn-group {
  border: 1px solid lightgrey;
  border-radius: 0;
}

.v-btn {
  text-transform: none !important;
  letter-spacing: unset;
}
</style>
