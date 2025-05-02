<template>
  <RijksoverheidCard
    v-if="availableChartLabels.length > 0"
    :title="title"
    :title-in-bar="true"
    ><div class="text-center">
      <RidButton
        v-for="(c, index) in availableChartLabels"
        :key="c"
        :class="{
          'button-toggle': index != availableChartLabels.length - 1,
          toggled: selectedChart == c,
        }"
        :aria-current="selectedChart == c ? 'true' : 'false'"
        variant="flat"
        :color="selectedChart == c ? 'primaryDark' : 'tertiary'"
        :value="c"
        @click="selectedChart = c"
        >{{ c }}</RidButton
      >
    </div>
    <img
      v-if="fundedByEU"
      alt="Gefinancierd Door de Europese Unie"
      :src="fundedByEUIMG"
      class="funded-by-eu"
    />
    <RidChart
      v-if="selectedChart == 'Kosten'"
      :chart-data="seriesKosten"
      label-horizontal="Datum"
      label-horizontal-table="Datum"
      label-measure="Miljoen (€)"
      x-data-type="date"
      y-data-type="currency-million"
      title="Kosten"
    />
    <RidChart
      v-else-if="selectedChart == 'Doorlooptijd'"
      :chart-data="seriesDoorlooptijd"
      label-horizontal="Datum"
      label-horizontal-table="Datum"
      label-measure="Maanden"
      x-data-type="date"
      y-data-type="number"
      title="Doorlooptijd"
    />

    <IndicatorLijstExpansion
      :indicator-lijst-namen="[
        IndicatorlijstNamen.DOORLOOPTIJD_EN_KOSTEN,
        IndicatorlijstNamen.MIJLPALEN,
      ]"
      :project="project"
    />
  </RijksoverheidCard>
</template>

<script setup lang="ts">
import type { LineChartDatapoint } from "@/types/chart"
import RidChart from "@/components/charts/RidChart.vue"
import cmsConfig from "@/config/cms"
import { getMonthsDifferenceBetweenDates, getObjectKeys } from "@/util"
import { flattenArray } from "@/util"
import RijksoverheidCard from "@/components/RidCol.vue"
import IndicatorLijstExpansion from "./IndicatorLijstTabel/IndicatorLijstExpansion.vue"
import {
  IndicatorlijstNamen,
  type ProjectMetAlleMetricsEnIndicatorLijsten,
} from "@/api-new"
import { useIndicatorLijst } from "@/composables/useIndicatorLijst"
import RidButton from "@/components/RidButton.vue"
import fundedByEUIMG from "../../../public/img/project/gefinancierd-door-eu.png"

const props = defineProps<{
  project: ProjectMetAlleMetricsEnIndicatorLijsten
  startDatum?: Date
}>()

const seriesIndicatoren = cmsConfig.general.kostenSeriesIndicatoren
const title = "Kosten en doorlooptijd"

const project = toRef(props, "project")
const { getIndicatorLijst } = useIndicatorLijst(project)
const indicatorLijst = computed(() =>
  getIndicatorLijst(IndicatorlijstNamen.DOORLOOPTIJD_EN_KOSTEN),
)

const formulieren = computed(() => indicatorLijst.value?.Formulier || [])

const fundedByEU = computed(() => {
  const mostRecentForm = [...formulieren.value].reduce((previous, current) => {
    return previous.FormulierAanmaakDatum < current.FormulierAanmaakDatum
      ? current
      : previous
  })
  return mostRecentForm.FormulierWaardes.some(
    (indicator) =>
      indicator.IndicatorTitel === "Gefinancierd door de Europese Unie" &&
      indicator.Waarde === "Ja",
  )
})

const seriesKosten = computed(() => {
  const datapoints = formulieren.value.map((f) => {
    const formulierDict = f.Dict

    const indicatorTitels = Object.keys(seriesIndicatoren)

    return indicatorTitels
      .map((indicatorTitel) => {
        const indicatorWaarde = formulierDict
          ? formulierDict[indicatorTitel]
          : undefined

        const yValue =
          typeof indicatorWaarde == "number"
            ? indicatorWaarde
            : parseFloat(indicatorWaarde)

        const datapoint: LineChartDatapoint = {
          x: formulierDict
            ? formulierDict[
                cmsConfig.general.indicatorTitelDatumDoorlooptijdEnKosten
              ]
            : "-",
          y: yValue,
          label: seriesIndicatoren[indicatorTitel],
        }
        return datapoint
      })
      .filter((datapoint) => {
        return (
          datapoint.y !== null &&
          typeof datapoint.y == "number" &&
          !isNaN(datapoint.y)
        )
      })
  })
  return flattenArray(datapoints)
})

const seriesDoorlooptijd = computed(() => {
  const doorlooptijdValues = formulieren.value.map((f) => {
    const datumString = f.FormulierWaardes.find(
      (w) =>
        w.IndicatorTitel ==
        cmsConfig.general.indicatorTitelDatumDoorlooptijdEnKosten,
    )?.Waarde

    const geschatteEindDatumString = f.FormulierWaardes.find(
      (w) => w.IndicatorTitel == "Actueel geschatte einddatum",
    )?.Waarde

    const datum = datumString ? new Date(datumString) : undefined

    const geschatteEindDatum = geschatteEindDatumString
      ? new Date(geschatteEindDatumString)
      : undefined

    let elapsedDelta = 0
    if (datum && props.startDatum) {
      elapsedDelta = getMonthsDifferenceBetweenDates(props.startDatum, datum)
    }

    let estimatedTotalDelta = 0
    if (geschatteEindDatum && props.startDatum) {
      estimatedTotalDelta = getMonthsDifferenceBetweenDates(
        props.startDatum,
        geschatteEindDatum,
      )
    }

    return [
      {
        x: datumString,
        y: elapsedDelta,
        label: "Gerealiseerde doorlooptijd (maanden)",
      },
      {
        x: datumString,
        y: estimatedTotalDelta,
        label: "Geschatte totale doorlooptijd (maanden)",
      },
    ] as LineChartDatapoint[]
  })
  return flattenArray(doorlooptijdValues)
})

const availableChartLabels = computed(() => {
  const labelsSeries = {
    Kosten: seriesKosten,
    Doorlooptijd: seriesDoorlooptijd,
  }

  const labelsSeriesKeys = getObjectKeys(labelsSeries)

  return labelsSeriesKeys.reduce((arr: string[], label) => {
    if (labelsSeries[label].value.length > 0) arr.push(label)
    return arr
  }, [])
})

const selectedChart = ref<string | null>(null)

watch(
  availableChartLabels,
  (newValue) => {
    if (newValue.length > 0) {
      selectedChart.value = newValue[0]
    }
  },
  { immediate: true },
)
</script>

<style scoped lang="scss">
@import "@/styles/_colors.scss";

.button-toggle {
  border-right-width: 0;
}

.funded-by-eu {
  float: right;
  width: 14em;
}
@media (max-width: 600px) {
  .funded-by-eu {
    width: 6em;
    margin: 12px 0;
  }
}
</style>
