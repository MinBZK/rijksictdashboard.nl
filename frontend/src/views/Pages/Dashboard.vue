<template>
  <Spinner v-if="!dashboardInitialized" />
  <template v-else>
    <TextLoaderContent
      content-group="Dashboard"
      content-field-key="DashboardIntro"
    />
    <RidRow
      ><v-col :cols="12" :md="6"><SearchBar /></v-col
    ></RidRow>
    <RidRow
      :title="getContent('Dashboard', 'DashboardKop').value"
      :caption="getContent('Dashboard', 'DashboardKopSubtitel').value"
    >
      <v-col :cols="12" :lg="5">
        <Dropdown
          v-model="selectedMinisterie"
          :items="
            ministeries.map((m) => {
              return { title: m.Naam, value: m.Naam }
            })
          "
          item-label="naam"
          label="Selecteer een ministerie"
          select-none-label="Alle ministeries"
          :allow-none="true"
        /> </v-col
    ></RidRow>

    <ScreenreaderMessageLiveArea>{{
      screenreaderMessage
    }}</ScreenreaderMessageLiveArea>

    <Metrics
      :filters="
        selectedMinisterie
          ? [
              {
                attribute: 'MinisterieNaam',
                values: [selectedMinisterie],
              },
            ]
          : []
      "
      :hidden-charts="['Doorlooptijd (aantallen)']"
      :show-ict-kosten="false"
      :auto-load="false"
      :show-full-title="false"
      :expandable-charts="false"
      :show-charts="false"
      :introduction-text-with-link="false"
      :is-home-page="false"
    />

    <RidRow
      ><LaatstGewijzigdeActiviteit
        :ministerie="selectedMinisterie"
        class="mb-4"
    /></RidRow>

    <RidRow>
      <RidCol
        :title="getContent('Grafieken', 'GestartBeëindigdTitel').value"
        :md="6"
        :sm="12"
        :title-in-bar="false"
        title-level="h3"
        :fill-height="true"
      >
        <GestartBeeindigd
          :ministerie="selectedMinisterie"
          :title="getContent('Grafieken', 'GestartBeëindigdTitel').value"
        />
      </RidCol>

      <RidCol
        :sm="6"
        :md="3"
        :title="getContent('Dashboard', 'StatusverdelingTitel').value"
        :subtitle="getContent('Dashboard', 'StatusverdelingSubtitel').value"
        :title-in-bar="false"
        title-level="h3"
        :fill-height="true"
      >
        <Statusverdeling :ministerie="selectedMinisterie" />
      </RidCol>

      <RidCol
        :sm="6"
        :md="3"
        :title="getContent('Dashboard', 'SchattingTotaleKostenTitel').value"
        :subtitle="
          getContent('Dashboard', 'SchattingTotaleKostenSubtitel').value
        "
        :title-in-bar="false"
        :fill-height="true"
        title-level="h3"
      >
        <KostenInitieelActueel
          :ministerie="selectedMinisterie"
          :auto-load="false"
        />
      </RidCol>
    </RidRow>

    <RidRow>
      <RidCol
        :cols="12"
        :md="4"
        :title="getContent('Dashboard', 'GewijzifdeIctActiviteiten').value"
        :title-in-bar="false"
        :fill-height="true"
        title-level="h3"
      >
        <GewijzigdeActiviteiten :ministerie="selectedMinisterie" />
      </RidCol>
      <MetricsChart
        :cols="12"
        :md="8"
        chart-name="Doorlooptijd (aantallen)"
        :ministerie-naam="selectedMinisterie"
        :auto-load="false"
      />
    </RidRow>
    <RidRow
      :allow-hide="true"
      show-more-label="Redenen voor grote verandering in ICT-activiteit"
    >
      <MetricsChart
        :lg="12"
        :sm="12"
        chart-name="Herijkingen aantal per redenen"
        :ministerie-naam="selectedMinisterie"
        :auto-load="false"
      />
    </RidRow>
  </template>
</template>

<script setup lang="ts">
import Metrics from "@/views/Common/Metrics.vue"
import KostenInitieelActueel from "@/views/Home/KostenInitieelActueel.vue"
import MetricsChart from "@/views/Common/MetricsChart.vue"
import GewijzigdeActiviteiten from "@/views/Home/GewijzigdeActiviteiten.vue"
import Statusverdeling from "@/views/Home/Statusverdeling.vue"
import GestartBeeindigd from "@/views/Home/GestartBeeindigd.vue"
import LaatstGewijzigdeActiviteit from "@/views/Home/LaatstGewijzigdeActiviteit.vue"
import RidRow from "@/components/RidRow.vue"
import RidCol from "@/components/RidCol.vue"
import Spinner from "@/components/Spinner.vue"
import SearchBar from "@/views/SearchBar.vue"
import { useMetrics } from "@/composables/useMetrics"
import { useTextLoader } from "@/composables/useTextLoader"
import type { ProjectFilter } from "@/types/project"
import Dropdown from "@/components/Dropdown.vue"
import { useMinisterie } from "@/composables/useMinisterie"
import ScreenreaderMessageLiveArea from "@/components/ScreenreaderMessageLiveArea.vue"
import TextLoaderContent from "@/components/TextLoaderContent.vue"

const { getContent } = useTextLoader()

const { ministeries } = useMinisterie()

const selectedMinisterie = ref<string | undefined>(undefined)

const screenreaderMessage = computed(() => {
  return selectedMinisterie.value === null ||
    typeof selectedMinisterie.value === "undefined"
    ? "Op het dashboard wordt nu data weergegeven van alle ministeries."
    : `Je hebt gekozen voor het ministerie van ${selectedMinisterie.value}. De informatie op dit dashboard zoals de kengetallen en de grafieken zijn nu aangepast voor alleen dit ministerie.`
})
const dashboardInitialized = ref<boolean>(false)
const loadingAny = computed(() => loadingActive.value || loadingAll.value)

const filters = computed(() => {
  const filters: ProjectFilter[] = selectedMinisterie.value
    ? [{ attribute: "MinisterieNaam", values: [selectedMinisterie.value] }]
    : []
  return filters
})

const { getData: getDataActive, loading: loadingActive } = useMetrics({
  filters,
  statusType: "allActive",
  autoLoad: false,
})

const { getData: getDataAll, loading: loadingAll } = useMetrics({
  filters,
  statusType: "all",
  autoLoad: false,
})

watch(
  selectedMinisterie,
  async () => {
    await Promise.all([getDataActive(), getDataAll()])
  },
  {
    immediate: true,
  },
)

watch(
  loadingActive,
  () => {
    if (!loadingActive && !loadingAll) dashboardInitialized.value = true
  },
  {
    immediate: true,
  },
)

watch(
  loadingAny,
  () => {
    if (!loadingAny.value) dashboardInitialized.value = true
  },
  {
    immediate: true,
  },
)
</script>

<style scoped lang="scss">
@import "@/styles/main.scss";
</style>
