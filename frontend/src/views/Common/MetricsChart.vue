<template>
  <RidCol
    :has-border="hasBorder"
    :title="title"
    :title-in-bar="false"
    title-level="h3"
  >
    <RidChart
      v-if="!loading && config && chartSeries.length > 0"
      :chart-data="chartSeries"
      :label-horizontal="config.labelHorizontal"
      :label-horizontal-table="config.labelHorizontal"
      :label-measure="config.labelMeasure"
      :chart-type="config.chartType"
      x-data-type="string"
      y-data-type="number"
      ordering="numerical"
      :caption="config.caption"
      :caption-position="config.captionPosition"
      :y-axis-integer="config.yAxisInteger"
      :data-labels="config.dataLabels"
      :title="config.title"
    />
    <span v-if="!loading && chartSeries.length == 0">
      Er is geen data beschikbaar voor deze grafiek.
    </span>
  </RidCol>
</template>

<script setup lang="ts">
import RidChart from "@/components/charts/RidChart.vue"
import type { LineChartDatapoint } from "@/types/chart"
import type { MetricsNumbersKey } from "@/types/metrics"
import { useMetrics } from "@/composables/useMetrics"
import { getMetricChartConfig } from "@/config/charts"
import RidCol from "@/components/RidCol.vue"
import type { Metrics } from "@/api-new"
import type { ProjectFilter } from "@/types/project"

const props = withDefaults(
  defineProps<{
    chartName: MetricsNumbersKey
    ministerieNaam?: string
    onderwerp?: string
    hasBorder?: boolean
    autoLoad?: boolean
    metricsData?: Metrics
    loading?: boolean
  }>(),
  {
    hasBorder: true,
    autoLoad: true,
  },
)

const config = computed(() => {
  const metricConfig = getMetricChartConfig()
  return metricConfig[props.chartName]
})

const title = computed(() => (config.value ? config.value.title : undefined))

const chartSeries = computed(() => {
  const data = metrics.value?.kengetallen?.[props.chartName]

  const xAxisSorting = config.value?.xAxisSorting

  const series = data
    ? Object.keys(data).map((xLabel) => {
        const getSortValue = () => {
          if (props.chartName == "Geschatte kosten per categorie") {
            return parseFloat(xLabel.replace(/[^0-9&-]/g, "").split("-")[0])
          } else if (xAxisSorting) {
            return xAxisSorting.indexOf(xLabel)
          } else {
            return xLabel
          }
        }

        const sortValue = getSortValue()

        return {
          x: xLabel,
          y: data[xLabel],
          label: "Aantal ICT-activiteiten",
          sortValue:
            typeof sortValue == "number" && isNaN(sortValue) ? -1 : sortValue,
        } as LineChartDatapoint
      })
    : []
  return series
})

const filters = computed(() => {
  const _filters: ProjectFilter[] = []
  if (props.ministerieNaam) {
    _filters.push({
      attribute: "MinisterieNaam",
      values: [props.ministerieNaam],
    })
  }
  if (props.onderwerp) {
    _filters.push({ attribute: "Onderwerp", values: [props.onderwerp] })
  }
  return _filters
})

const metricsFromSource = useMetrics({
  filters,
  statusType: "allActive",
  autoLoad: props.autoLoad,
})

const metrics = computed(() => {
  if (props.metricsData) {
    return props.metricsData
  } else {
    return metricsFromSource.metrics.value
  }
})

const loading = computed(() => {
  if (props.loading !== undefined) {
    return props.loading
  } else {
    return metricsFromSource.loading.value
  }
})
</script>
