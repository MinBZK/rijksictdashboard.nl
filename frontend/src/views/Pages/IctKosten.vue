<template>
  <TextLoaderContent content-group="ICT-kosten" content-field-key="Deel 1" />
  <TextLoaderContent
    content-group="ICT-kosten"
    content-field-key="Deel 2"
    title="Inschatting van de verdeling"
    :expandable="true"
  />

  <RidRow>
    <v-col :md="3" :xs="12">
      <Dropdown
        v-model="selectedYear"
        :items="
          allYears.map((y) => {
            return { title: y, value: y }
          })
        "
        label="Selecteer een jaar"
      />
    </v-col>

    <v-col :md="3" :xs="12">
      <Dropdown
        v-model="selectedMinisterie"
        :items="
          allMinisteries.map((m) => {
            return { title: m, value: m }
          })
        "
        label="Selecteer een ministerie"
        select-none-label="Alle ministeries"
        :allow-none="true"
      />

      <ScreenreaderMessageLiveArea>{{
        screenreaderMessage
      }}</ScreenreaderMessageLiveArea>
    </v-col>
  </RidRow>
  <RidRow
    v-show="sumCostsKV > 0 && initialized"
    :title="getChartTitle('kas-verplichtingenstelsel')"
  >
    <RidCol :lg="3" :fill-height="true"
      ><RidCardMetricContent
        :title="getContent('ICT-kosten', 'kostenTotaalKV').value"
        data-type="string"
        unit-suffix="mln."
        :max-digits="10"
        :metric-value="sumCostsKV"
    /></RidCol>
    <RidCol key="col1" :lg="9">
      <RidChart
        v-if="chartDataKV.length > 0"
        :chart-data="chartDataKV"
        chart-type="barChart"
        :label-horizontal="xLabel"
        :label-horizontal-table="xLabel"
        label-measure="Miljoen (€)"
        x-data-type="string"
        y-data-type="currency-million"
        :type="chartType1"
        :title="getChartTitle('kas-verplichtingenstelsel')"
      ></RidChart>
    </RidCol>
    <ExpandContent v-show="showTable" title="Uitgaven in tabelvorm">
      <RidCol>
        <IctKostenTable :table-data="tableDataKV" />
      </RidCol>
    </ExpandContent>
  </RidRow>
  <RidRow
    v-show="sumCostsBL > 0 && initialized"
    :title="getChartTitle('baten-lastenstelsel')"
  >
    <RidCol :lg="3" :fill-height="true"
      ><RidCardMetricContent
        :title="getContent('ICT-kosten', 'kostenTotaalBL').value"
        data-type="string"
        unit-suffix="mln."
        :max-digits="10"
        :metric-value="sumCostsBL"
    /></RidCol>
    <RidCol key="col2" :lg="9">
      <RidChart
        v-if="chartDataBL.length > 0"
        :chart-data="chartDataBL"
        chart-type="barChart"
        :label-horizontal="xLabel"
        :label-horizontal-table="xLabel"
        label-measure="Miljoen (€)"
        x-data-type="string"
        y-data-type="currency-million"
        :type="chartType1"
        :title="getChartTitle('baten-lastenstelsel')"
      ></RidChart>
    </RidCol>
    <ExpandContent v-show="showTable" title="Kosten in tabelvorm">
      <RidCol>
        <IctKostenTable :table-data="tableDataBL" />
      </RidCol>
    </ExpandContent>
  </RidRow>
</template>

<script setup lang="ts">
import RidRow from "@/components/RidRow.vue"
import RidCol from "@/components/RidCol.vue"
import IctKostenTable from "@/views/Pages/IctKostenTable.vue"
import RidCardMetricContent from "@/components/RidCardMetricContent.vue"
import RidChart from "@/components/charts/RidChart.vue"
import { getIctKosten } from "@/services/ictkosten"
import TextLoaderContent from "@/components/TextLoaderContent.vue"
import type { IctKosten } from "@/types/ictkosten"
import { useTextLoader } from "@/composables/useTextLoader"
import Dropdown from "@/components/Dropdown.vue"
import ScreenreaderMessageLiveArea from "@/components/ScreenreaderMessageLiveArea.vue"
import ExpandContent from "@/components/ExpandContent.vue"

const { getContent } = useTextLoader()

const showTable = computed(() => !selectedMinisterie.value)

const selectedMinisterie = ref<string | null>(null)
let selectedYear = ref<number | null>(null)

const screenreaderMessage = computed(() => {
  return selectedMinisterie.value === null || selectedMinisterie.value === ""
    ? "De ICT-kosten worden nu weergegeven van alle ministeries."
    : `Je hebt gekozen voor het ministerie van ${selectedMinisterie.value}. De ICT-kosten worden weergegeven voor alleen dit ministerie.`
})

const initialized = ref<boolean>(false)

const kostenData = ref<{ [key: number]: IctKosten } | null>(null)

const getData = async () => {
  kostenData.value = await getIctKosten(selectedMinisterie.value)
  initialized.value = true
}

const selectedData = computed(() =>
  kostenData.value && selectedYear.value
    ? kostenData.value[selectedYear.value]
    : null,
)
const chartDataKV = computed(() => selectedData.value?.graph_data_kv || [])
const chartDataBL = computed(() => selectedData.value?.graph_data_bl || [])
const tableDataKV = computed(
  () => selectedData.value?.kosten_kasverplichtingenstelsel || [],
)
const tableDataBL = computed(
  () => selectedData.value?.kosten_batenlastenstelsel || [],
)
const sumCostsKV = computed(() =>
  Math.round(
    chartDataKV.value.reduce((accumulator, currentValue) => {
      return (
        accumulator +
        (currentValue.y ? parseFloat(currentValue.y.toString()) : 0)
      )
    }, 0),
  ),
)

const sumCostsBL = computed(() =>
  Math.round(
    chartDataBL.value.reduce((accumulator, currentValue) => {
      return (
        accumulator +
        (currentValue.y ? parseFloat(currentValue.y.toString()) : 0)
      )
    }, 0),
  ),
)

const allMinisteries = computed(
  () => selectedData.value?.available_ministeries || [],
)

const allYears = computed(() =>
  kostenData.value ? Object.keys(kostenData.value).sort() : [],
)

getData()

watch(selectedMinisterie, () => {
  getData()
})

watch(allYears, () => {
  if (!selectedYear.value)
    selectedYear.value = parseInt([...allYears.value].reverse()[0])
})

const chartType1 = computed(() => {
  return selectedMinisterie.value === null ? "stacked" : "grouped"
})

const xLabel = computed(() => {
  return selectedMinisterie.value === null ? "Ministerie" : "Kostenpost"
})

const getChartTitle = (stelsel: string) =>
  selectedMinisterie.value === null
    ? `ICT-${
        stelsel === "baten-lastenstelsel" ? "kosten" : "uitgaven"
      } volgens het ${stelsel} per ministerie`
    : `${selectedMinisterie.value} - ICT-${
        stelsel === "baten-lastenstelsel" ? "kosten" : "uitgaven"
      } volgens het ${stelsel}`
</script>

<style scoped lang="scss">
@import "@/styles/main.scss";
</style>
