<template>
  <v-row class="mb-7 mt-3" no-gutters>
    <RidButton
      v-if="hasChartData"
      :prepend-icon="icon"
      variant="outlined"
      class="mr-4"
      :class="xs && 'mb-1'"
      @click="showTable = !showTable"
      >{{ showTable ? "Toon grafiek" : "Toon datatabel" }}</RidButton
    >
    <ScreenreaderMessageLiveArea>{{
      showTable ? "De datatabel wordt getoond." : "De grafiek wordt getoond."
    }}</ScreenreaderMessageLiveArea>
    <RidButton
      v-if="caption && captionPosition == 'hidden'"
      ref="uitlegButton"
      prepend-icon="mdi-information-outline"
      :class="xs && 'mt-1'"
      variant="outlined"
      @click="showCaption = !showCaption"
      >{{ buttonLabel }}</RidButton
    >
    <RidDialog
      v-if="showCaption"
      :title="buttonLabel"
      :return-focus="uitlegButton?.focus"
      @close="showCaption = false"
    >
      <RidChartCaption v-if="caption" :caption="caption" />
    </RidDialog>
  </v-row>

  <slot name="chart-top" :show-table="showTable" />

  <v-row>
    <v-col
      :lg="hasCaption && captionPosition == 'right' ? 12 - captionWidth : 12"
      cols="12"
    >
      <component
        :is="HighchartsWrapper"
        v-bind="props"
        v-if="!showTable && hasChartData"
        :sorted-categories="uniqueSortedX"
      />
      <RidChartTable
        v-if="showTable && hasChartData"
        :unique-x="uniqueSortedX"
        :chart-data="chartData"
        :label-horizontal-table="labelHorizontalTable"
        :serie-names="serieNames"
        :x-data-type="xDataType"
        :y-data-type="yDataType"
        :default-sorting-type="defaultSorting"
      />
      <template v-if="!hasChartData">{{ noDataText }}</template>
    </v-col>
    <v-col
      v-if="caption && captionPosition == 'right'"
      cols="12"
      :lg="captionWidth"
    >
      <RidChartCaption v-if="caption" :caption="caption" />
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import type {
  ChartCaptionPosition,
  ChartDataLabel,
  ChartHorizontalLine,
  ChartType,
  LineChartDatapoint,
} from "@/types/chart"
import { useTheme, useDisplay } from "vuetify"
import HighchartsWrapper from "./HighchartsWrapper.vue"
import RidButton from "../RidButton.vue"
import RidChartTable from "./RidChartTable.vue"
import RidDialog from "@/components/RidDialog.vue"
import { sortArrayByKey } from "@/util"
import RidChartCaption from "./RidChartCaption.vue"
import ScreenreaderMessageLiveArea from "@/components/ScreenreaderMessageLiveArea.vue"
import type { ProjectAttributePrimitiveDataType } from "@/types/project"

const { xs } = useDisplay()

// copy pasted from HighchartsWrapper.vue, importing gives an error
type HighchartsProps = {
  chartData: LineChartDatapoint[]
  xDataType: ProjectAttributePrimitiveDataType
  yDataType: ProjectAttributePrimitiveDataType
  labelHorizontal: string
  labelHorizontalTable: string
  labelMeasure: string
  chartType?: ChartType
  type?: string
  colors?: string[]
  ordering?: string
  gap?: number
  sortedCategories?: string[]
  yAxisInteger?: boolean
  height?: number
  horizontalLine?: ChartHorizontalLine
  dataLabels?: ChartDataLabel
  title: string
  hideLegendIfOnlyOneSerie?: boolean
}

const props = withDefaults(
  defineProps<
    HighchartsProps & {
      caption?: string[] | string
      captionPosition?: ChartCaptionPosition
      noDataText?: string
    }
  >(),
  {
    chartType: "timeLine",
    type: "grouped",
    colors: () => {
      const colors = useTheme().current.value.colors
      return [
        colors.primary,
        colors.violet,
        colors.donkergeel,
        colors.groen,
        colors.paars,
        colors.robijnroodTint1,
        colors.geel,
        colors.mintgroen,
      ]
    },
    gap: 20,
    captionPosition: "hidden",
    noDataText: "Voor deze grafiek is geen data beschikbaar.",
    dataLabels: () => {
      return { enabled: true }
    },
  },
)

const defaultSorting = props.chartType === "pieChart" ? "yValue" : "xCategory"

const captionWidth = 5
const buttonLabel = "Uitleg over deze grafiek"
const hasCaption = computed(() => !!props.caption)
const showCaption = ref<boolean>(false)
const hasChartData = computed(() => props.chartData.length > 0)

const icon = computed(() => {
  return showTable.value ? "mdi-chart-bar" : "mdi-table"
})

const uniqueSortedX = computed(() => {
  const sortedChartData = sortArrayByKey(props.chartData, "sortValue")
  const values = sortedChartData.map((dp) => dp.x)
  return [...new Set(values)]
})

const serieNames = computed(() => {
  const values = props.chartData.map((datapoint) => datapoint.label)
  return [...new Set(values)]
})

let showTable = ref<boolean>(false)

const uitlegButton = ref<typeof RidButton | null>(null)
</script>

<style scoped lang="scss">
@import "@/styles/_colors.scss";
.barchart-container {
  width: 95%;
  height: 400px;
  position: relative;
  margin: auto;
}

tr {
  line-height: 0.5;
}
</style>
