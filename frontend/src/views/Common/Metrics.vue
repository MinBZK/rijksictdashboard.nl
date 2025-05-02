<template>
  <RidRow
    :title="title"
    :no-bottom-padding="expandableCharts && showCharts"
    :aria-label="`${title}. De waarden van kengetallen zijn links. Deze links brengen je naar de overzichtspagina van de ICT-activiteiten waar er gefilterd is op de relevante ICT-activiteiten.`"
    :title-level="titleLevel"
    :caption="
      getContent(
        'Home',
        introductionTextWithLink
          ? 'Introductie kengetallen'
          : 'Introductie kengetallen\tzonder link',
      ).value
    "
  >
    <template v-if="nActiviteiten > 0">
      <RidCol
        v-if="showIctKosten"
        :lg="4"
        :sm="6"
        :cols="12"
        :fill-height="true"
      >
        <RidCardMetricContent
          title="ICT-kosten"
          data-type="string"
          :metric-value="kengetallen?.['Meest recente jaar met kosten']"
          ><template #caption>
            <router-link :to="{ name: 'ict-kosten' }">
              Bekijk de ICT-kosten</router-link
            >
          </template></RidCardMetricContent
        >
      </RidCol>
      <RidCol
        v-for="mK in getObjectKeys(metricsConfig)"
        :key="mK"
        :cols="12"
        :sm="6"
        :lg="showIctKosten ? 4 : 3"
        :fill-height="true"
        :has-five-columns="false"
      >
        <RidCardMetricContent
          :title="metricsConfig[mK]?.label || mK"
          :data-type="metricsConfig[mK]?.dataType"
          :unit-suffix="metricsConfig[mK]?.unitSuffix"
          :max-digits="metricsConfig[mK]?.maximumDigits"
          :metric-value="kengetallen?.[mK]"
          :caption="metricsConfig[mK]?.caption"
          :filters="[...metricsConfig[mK]?.filters, ...filters]"
          :sorting="metricsConfig[mK]?.sorting || []"
          :fixed-title-height="true"
        ></RidCardMetricContent>
      </RidCol>
    </template>
    <template v-else>
      <v-col class="mb-5">Er zijn geen activiteiten in uitvoering.</v-col>
    </template>
  </RidRow>
  <RidRow
    v-if="metrics && nActiviteiten > 0 && showCharts"
    :allow-hide="expandableCharts"
  >
    <MetricsChart
      v-for="chartName in displayedCharts"
      :key="chartName"
      :chart-name="chartName"
      :metrics-data="metrics"
      :loading="loading"
      :ministerie-naam="ministerieNaam"
      label="Aantal activiteiten"
      :auto-load="false"
    />
  </RidRow>
</template>

<script setup lang="ts">
import type { MetricsNumbersKey } from "@/types/metrics"
import type {
  AttributeSorting,
  ProjectAttributePrimitiveDataType,
  ProjectFilter,
} from "@/types/project"
import RidRow from "@/components/RidRow.vue"
import RidCol from "@/components/RidCol.vue"
import { useMetrics } from "@/composables/useMetrics"
import RidCardMetricContent from "@/components/RidCardMetricContent.vue"
import MetricsChart from "./MetricsChart.vue"
import { useTextLoader } from "@/composables/useTextLoader"
import type { TitleLevel } from "@/types/components"
import { getObjectKeys } from "@/util"

const { getContent } = useTextLoader()

const props = withDefaults(
  defineProps<{
    ministerieNaam?: string
    filters: ProjectFilter[]
    // onderwerp?: string
    hiddenCharts?: MetricsNumbersKey[]
    showIctKosten?: boolean
    autoLoad?: boolean
    showFullTitle?: boolean
    titleLevel?: TitleLevel
    expandableCharts?: boolean
    showCharts?: boolean
    introductionTextWithLink: boolean
    isHomePage?: boolean
  }>(),
  {
    hiddenCharts: () => [] as MetricsNumbersKey[],
    showIctKosten: false,
    autoLoad: true,
    showFullTitle: true,
    titleLevel: "h3",
    expandableCharts: true,
    showCharts: false,
  },
)

const displayedCharts = (
  [
    "Geschatte kosten per categorie",
    "Doorlooptijd (aantallen)",
  ] as MetricsNumbersKey[]
).filter((chartType) => !props.hiddenCharts.includes(chartType))

const filters = toRef(props, "filters")

const { metrics, loading } = useMetrics({
  statusType: "allActive",
  autoLoad: props.autoLoad,
  filters,
})

const kengetallen = computed(() => metrics.value?.kengetallen)

const nActiviteiten = computed(
  () => metrics.value?.kengetallen["Aantal grote ICT-activiteiten"],
)

const title = computed(() =>
  props.showFullTitle ? "ICT-activiteiten" : "Kengetallen",
)

type MetricConfig = {
  dataType: ProjectAttributePrimitiveDataType
  label?: string
  unitSuffix?: string
  maximumDigits?: number
  caption?: string
  filters?: ProjectFilter[]
  sorting?: AttributeSorting[]
}

const metricsConfig: Partial<Record<MetricsNumbersKey, MetricConfig>> =
  reactive({
    "Aantal grote ICT-activiteiten": {
      dataType: "integer",
      label: "ICT-activiteiten in uitvoering",
      caption: getContent(
        "Dashboard",
        "ToelichtingAantalActiviteitenInUitvoering",
      ).value,
      filters: [
        {
          attribute: "ProjectStatus",
          values: ["In uitvoering", "In heroriëntatie"],
        },
      ],
    },
    "DoorlooptijdActueel (mean)": {
      dataType: "number",
      label: "Duurt gemiddeld",
      unitSuffix: "jaar",
      maximumDigits: 1,
      caption: getContent("Dashboard", "ToelichtingDoorlooptijd").value,
      filters: [
        {
          attribute: "ProjectStatus",
          values: ["In uitvoering", "In heroriëntatie"],
        },
      ],
      sorting: [
        {
          attribute: "DoorlooptijdActueel",
          direction: "desc",
        },
      ],
    },
    ...(!props.isHomePage
      ? {
          "SchattingTotaleKostenHuidigJaar (sum)": {
            dataType: "currency",
            unitSuffix: "mln.",
            label: "Schatting totale kosten",
            maximumDigits: 0,
            caption: getContent("Dashboard", "ToelichtingSchattingTotaleKosten")
              .value,
            filters: [
              {
                attribute: "ProjectStatus",
                values: ["In uitvoering", "In heroriëntatie"],
              },
            ],
            sorting: [
              {
                attribute: "SchattingTotaleKostenHuidigJaar",
                direction: "desc",
              },
            ],
          },
        }
      : {}),
    "Aantal AcICT-adviezen": {
      dataType: "integer",
      label: "ICT-activiteiten met ten minste 1 AcICT-advies",
      caption: getContent("Dashboard", "ToelichtingBit").value,
      filters: [
        { attribute: "HeeftAcICTAdvies", values: ["Ja"] },
        {
          attribute: "ProjectStatus",
          values: ["In uitvoering", "In heroriëntatie"],
        },
      ],
    },
    ...(props.isHomePage
      ? {
          "Aantal afgeronde activiteiten": {
            dataType: "integer",
            label: "ICT-activiteiten afgerond",
            caption: getContent(
              "Dashboard",
              "ToelichtingAantalActiviteitenAfgerond",
            ).value,
            filters: [
              {
                attribute: "ProjectStatus",
                values: ["Afgerond"],
              },
            ],
          },
        }
      : {}),
  })
</script>

<style lang="scss" scoped>
div.v-card:deep(.v-card-title) {
  white-space: normal;
  text-overflow: unset;
}

div.v-card-item {
  grid-template-rows: 1fr min-content;
}
</style>
