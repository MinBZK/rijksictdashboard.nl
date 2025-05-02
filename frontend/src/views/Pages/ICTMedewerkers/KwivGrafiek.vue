<template>
  <RidRow :title="chartTitle">
    <RidCol :lg="6" :has-border="false" :no-padding="true">
      <Dropdown
        v-model="selectedMinisterie"
        :items="
          kwivData?.available_ministeries.map((m) => {
            return {
              title: m,
              value: m,
            }
          }) || []
        "
        label="Selecteer een ministerie"
        select-none-label="Alle ministeries"
        :allow-none="true"
      />

      <ScreenreaderMessageLiveArea>{{
        screenreaderMessage
      }}</ScreenreaderMessageLiveArea>
    </RidCol>
    <RidCol :lg="6" :has-border="false" :no-padding="true">
      <Dropdown
        v-model="selectedCategory"
        :items="
          kwivData?.available_categories.map((c) => {
            return { title: c, value: c }
          }) || []
        "
        label="Selecteer een categorie"
        select-none-label="Alle categorieën"
        :allow-none="true"
      />
    </RidCol>
    <RidCol key="col1" :lg="12">
      <RidChart
        v-if="chartData.length > 0"
        :chart-data="chartData"
        chart-type="HorizontalBarChart"
        :label-horizontal="xLabel"
        :label-horizontal-table="xLabel"
        label-measure="Aantal"
        x-data-type="string"
        y-data-type="number"
        :title="chartTitle"
        :height="600"
        :hide-legend-if-only-one-serie="false"
      ></RidChart>
    </RidCol>
  </RidRow>
</template>

<script setup lang="ts">
import { getKwivData } from "@/services/kwiv"
import RidCol from "@/components/RidCol.vue"
import RidRow from "@/components/RidRow.vue"
import RidChart from "@/components/charts/RidChart.vue"
import type { KWIVData, KwivJaar } from "@/api-new"
import type { LineChartDatapoint } from "@/types/chart"
import ScreenreaderMessageLiveArea from "@/components/ScreenreaderMessageLiveArea.vue"
import Dropdown from "@/components/Dropdown.vue"

const props = defineProps<{
  jaar: KwivJaar
  title: string
}>()

const selectedMinisterie = ref<string>()
const selectedCategory = ref<string>()

const xLabel = computed(() => {
  return `${!selectedMinisterie.value ? "Ministerie" : "Categorie"}`
})

const chartTitle = computed(() => {
  return `${props.title} (stand van zaken: 31-12-${props.jaar}${
    selectedMinisterie.value ? "; " + selectedMinisterie.value : ""
  }${selectedCategory.value ? "; " + selectedCategory.value : ""})`
})

const kwivData = ref<KWIVData | undefined>(undefined)

const chartData = computed(() =>
  (kwivData.value?.datapoints || []).map((d) => {
    const datapoint = d as LineChartDatapoint
    datapoint.sortValue = datapoint.x
    return datapoint
  }),
)

const getData = async () => {
  kwivData.value = await getKwivData({
    ministerie: selectedMinisterie.value,
    jaar: props.jaar,
    category: selectedCategory.value,
  })
}

watch(
  selectedMinisterie,
  () => {
    getData()
  },
  {
    immediate: true,
  },
)

watch(selectedCategory, () => {
  getData()
})

const screenreaderMessage = computed(() => {
  return `${
    !selectedMinisterie.value
      ? "De grafiek toont het aantal medewerkers met een KWIV profiel per ministerie."
      : `Je hebt gekozen voor het ministerie van ${selectedMinisterie.value}. De grafiek toont het aantal medewerkers met een KWIV profiel nu voor alleen dit ministerie.`
  }`
})
</script>
