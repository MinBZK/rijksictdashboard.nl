<template>
  <RidRow :title="title" title-level="h3">
    <RidCol>
      <RidChart
        :chart-data="chartData"
        x-data-type="string"
        y-data-type="number"
        label-horizontal-table="Meting"
        label-measure="Percentage"
        label-horizontal="Meting"
        chart-type="barChart"
        :title="title"
        :data-labels="{
          enabled: true,
          value: 'y',
        }"
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
  "0-meting (2021)": [1.9],
  "1-meting (2022)": [2.1],
  "2-meting (2023)": [2.3],
}

const title = "Gemiddeld volwassenheidsniveau"

const chartData = computed((): LineChartDatapoint[] => {
  const datapoints = Object.keys(sourceData).reduce(
    (arr: LineChartDatapoint[], xLabel) => {
      const xLabelDatapoints = sourceData[xLabel].map((d) => {
        return {
          x: xLabel,
          y: d,
          label: "Volwassenheidsniveau",
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
