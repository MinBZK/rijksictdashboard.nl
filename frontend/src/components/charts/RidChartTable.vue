<template>
  <RidTable
    :table-data="chartTableData"
    :columns="columnConfig"
    :default-sorting="defaultSorting"
    :column-sequence="columnSequence"
  />
</template>

<script setup lang="ts">
import type { LineChartDatapoint } from "@/types/chart"
import type { ProjectAttributePrimitiveDataType } from "@/types/project"
import { computed } from "vue"
import RidTable from "@/components/RidTable.vue"
import type { TableConfig } from "@/types/table"

const props = withDefaults(
  defineProps<{
    uniqueX: string[]
    labelHorizontalTable: string
    chartData: LineChartDatapoint[]
    serieNames: string[]
    xDataType: ProjectAttributePrimitiveDataType
    yDataType: ProjectAttributePrimitiveDataType
    defaultSortingType: "xCategory" | "yValue"
  }>(),
  {
    defaultSortingType: "xCategory",
  },
)

const defaultSorting = computed(() => {
  if (props.defaultSortingType == "xCategory") {
    return { header: props.labelHorizontalTable, ascending: true }
  } else {
    return { header: props.serieNames[0], ascending: false }
  }
})

const chartTableData = computed(() => {
  return props.uniqueX.map((uX) => {
    return {
      [props.labelHorizontalTable]: uX,
      ...props.serieNames.reduce(
        (obj: Record<string, string | number>, serieName) => {
          obj[serieName] =
            props.chartData.find(
              (datapoint) => datapoint.x == uX && datapoint.label == serieName,
            )?.y || 0
          return obj
        },
        {},
      ),
    }
  })
})

type RowData = Record<string, string | number | null | undefined>

const columnConfig = computed((): TableConfig<RowData>[] => {
  const config: TableConfig<RowData>[] = [
    {
      key: props.labelHorizontalTable,
      dataType: props.xDataType,
    },
    ...props.serieNames.map((serieName) => ({
      key: serieName,
      dataType: props.yDataType,
    })),
  ]
  return config
})

const columnSequence = computed(() => {
  return [props.labelHorizontalTable, ...props.serieNames]
})
</script>

<style scoped lang="scss">
:deep(.v-table__wrapper table) {
  width: auto !important;
}
</style>
