<template>
  <RidChart
    :chart-data="gestartCount"
    chart-type="barChart"
    label-horizontal="Jaar"
    label-horizontal-table="Jaar"
    label-measure="Aantal ICT-activiteiten"
    x-data-type="string"
    y-data-type="number"
    :y-axis-integer="true"
    :caption="caption"
    :title="title"
  ></RidChart>
</template>

<script setup lang="ts">
import { useMetrics } from "@/composables/useMetrics"
import type { LineChartDatapoint } from "@/types/chart"
import RidChart from "@/components/charts/RidChart.vue"
import { useTextLoader } from "@/composables/useTextLoader"
import type { ProjectFilter } from "@/types/project"

type ChartOptions = "Afgelopen 5 jaar" | "Alle jaartallen"
// const availableChartLabels: ChartOptions[] = [
//   "Afgelopen 5 jaar",
//   "Alle jaartallen",
// ]

const selectedChart = ref<ChartOptions>("Afgelopen 5 jaar")

const { getContent } = useTextLoader()

const caption = getContent("Grafieken", "GrafiekGestartBeëindigd")

const props = withDefaults(
  defineProps<{
    ministerie?: string
    autoLoad?: boolean
    title: string
  }>(),
  {
    autoLoad: false,
  },
)

const filters = computed(() => {
  const filters: ProjectFilter[] = props.ministerie
    ? [{ attribute: "MinisterieNaam", values: [props.ministerie] }]
    : []
  return filters
})

const { metrics } = useMetrics({
  filters,
  statusType: "all",
  autoLoad: props.autoLoad,
})

const gestartCount = computed(() => {
  const chartData = (metrics.value?.kengetallen?.[
    "Aantal gestarte activiteiten"
  ] || []) as LineChartDatapoint[]

  const currentYear = new Date().getFullYear()
  const labels = [...new Set(chartData.map((d) => d.label))]
  let aantalJaren = 5
  if (selectedChart.value == "Alle jaartallen") {
    const jaartallen = chartData.map((datapoint) => parseInt(datapoint.x))
    const minimumJaar =
      jaartallen.length > 0 ? Math.min(...jaartallen) : currentYear - 4
    aantalJaren = currentYear - minimumJaar + 1
  }

  return [...Array(aantalJaren).keys()]
    .map((year) =>
      labels.map((label) => {
        const yearLabel = (year + currentYear - (aantalJaren - 1)).toString()
        return {
          x: yearLabel,
          label,
          y:
            chartData.find((d) => d.label == label && d.x == yearLabel)?.y || 0,
        } as LineChartDatapoint
      }),
    )
    .flat()
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
