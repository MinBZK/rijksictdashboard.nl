<template>
  <RidRow :title="title" title-level="h3">
    <RidCol>
      <RidChart
        :chart-data="chartData"
        x-data-type="string"
        y-data-type="percentage"
        label-horizontal="Datacentrum"
        label-horizontal-table="Datacentrum"
        label-measure="Percentage"
        chart-type="barChart"
        :data-labels="{
          enabled: true,
          value: 'y',
        }"
        :horizontal-line="{
          label: '2030 doel',
          value: 50,
        }"
        :title="title"
      />
    </RidCol>
  </RidRow>
</template>

<script setup lang="ts">
import RidChart from "@/components/charts/RidChart.vue"
import type { LineChartDatapoint } from "@/types/chart"
import RidRow from "@/components/RidRow.vue"
import RidCol from "@/components/RidCol.vue"

const sourceData: Record<string, number[]> = {
  "ODC RWS-DJI": [0.79, 0.79, 0.8, 0.81, 0.82],
  "ODC Belastingdienst": [0.71, 0.72, 0.73, 0.73, 0.74],
  "ODC Haaglanden": [0.82, 0.81, 0.84, 0.83, 0.83],
  "ODC Noord": [0.82, 0.81, 0.81, 0.83, 0.8],
}

const startYear = 2018
const title = "Data center infrastructure efficiency (DCiE) per ODC"

const chartData = computed((): LineChartDatapoint[] => {
  const datapoints = Object.keys(sourceData).reduce(
    (arr: LineChartDatapoint[], xLabel) => {
      const xLabelDatapoints = sourceData[xLabel].map((d, index) => {
        return {
          x: xLabel,
          y: d * 100,
          label: Math.round(startYear + index).toString(),
          sortKey: xLabel,
        } as LineChartDatapoint
      })
      arr = [...arr, ...xLabelDatapoints]
      return arr
    },
    [],
  )

  return datapoints
})
</script>
