<template>
  <Page
    :title="project?.Naam.toString() || ''"
    :loading="loading"
    :error="errorMessage"
    :description="description"
  >
    <template #content-before>
      <v-alert
        v-if="
          project?.ProjectVersieStatusNaam != 'Gepubliceerd' &&
          !loading &&
          !errorMessage
        "
        type="warning"
        class="mb-5"
        icon="mdi-alert"
      >
        Deze versie is niet gepubliceerd (versie:
        {{ project?.ProjectVersie }}, status:
        {{ project?.ProjectVersieStatusNaam.toLowerCase() }}).
      </v-alert>
    </template>
    <template v-if="!loading && !errorMessage">
      <v-row v-if="!contentOnly">
        <v-col class="buttons mb-3">
          <RidButton
            ref="exportButton"
            type="submit"
            color="primaryDark"
            rounded="0"
            prepend-icon="mdi-download"
            class="text-none"
            variant="outlined"
            @click="showExportDialog = true"
            @keyup.enter="showExportDialog = true"
            >Exporteer</RidButton
          >
          <RidDialog
            v-if="showExportDialog"
            :activator="exportButton"
            :title="`Exporteer activiteit '${project?.Naam}'`"
            :return-focus="exportButton?.focus"
            @close="showExportDialog = false"
          >
            <v-row class="pa-0 ma-0"
              ><v-col class="pa-0"
                ><label for="export-formats">Kies bestandsformaat:</label>
              </v-col>
            </v-row>
            <v-row class="pa-0 ma-0"
              ><v-col class="px-0" cols="5">
                <div ref="selectFormat">
                  <dropdown-vanilla
                    id="export-formats"
                    v-model="selectedExportFormat"
                    :items="exportFormats"
                  />
                </div>
              </v-col>
              <v-col cols="3">
                <form
                  v-if="project"
                  class="block"
                  :action="
                    projectSpreadsheetUrl(
                      selectedExportFormat == ExportFormat.Excel
                        ? 'excel'
                        : 'ods',
                      project.ProjectId,
                    )
                  "
                >
                  <RidButton
                    type="submit"
                    color="primaryDark"
                    tabindex="0"
                    rounded="0"
                    prepend-icon="mdi-download"
                    class="text-none button-full-height"
                    block
                    >Download</RidButton
                  >
                </form>
              </v-col>
            </v-row>
          </RidDialog>
        </v-col>
      </v-row>
      <RidRow>
        <RidCol title="Algemene informatie" :lg="6" :title-in-bar="true">
          <IndicatorLijstTabel
            v-if="formulierAlgemeen"
            :indicator-lijst="getIndicatorLijst(IndicatorlijstNamen.ALGEMEEN)"
            :formulieren="formulierAlgemeen"
            :tiles="true"
            :indicator-titel-sequence="formulierAlgemeenIndicatorenSequence"
            :excluded-indicatoren="[
              'Dienstverlening 1',
              'Dienstverlening 2',
              'Dienstverlening 3',
            ]"
            :indicator-title-div-id="{
              'Heeft AcICT-advies gehad': {
                divId: 'documentatie',
                value: 'Ja',
              },
            }"
          />
          <v-col class="pa-0">
            <v-card variant="flat"
              ><v-card-text class="px-0 laatst-gewijzigd"
                ><v-icon icon="mdi-clock-outline" />&nbsp;Laatst gewijzigd op
                <FormattedValue
                  :value="project?.ProjectVersieWijzigingsDatum"
                  :format-config="{ dataType: 'date' }"
                />
              </v-card-text>
            </v-card>
          </v-col>
        </RidCol>

        <RidCol title="Samenvatting" :lg="6" :title-in-bar="true">
          <div
            v-for="summaryHeader in Object.keys(summary)"
            :key="summaryHeader"
            class="pa-0"
          >
            <h3>{{ summaryHeader }}</h3>
            <p class="mb-5">
              <FormattedValue
                :format-config="{ dataType: 'string' }"
                :value="summary[summaryHeader] || dataMissingLabel"
                :max-words="50"
                :value-title="summaryHeader"
              />
            </p>
          </div>
          <h3>Meerwaarde voor de samenleving</h3>
          <IndicatorLijstButton
            v-if="getIndicatorLijst(IndicatorlijstNamen.MAATSCHAPPELIJKE_BATEN)"
            :indicator-lijst-naam="IndicatorlijstNamen.MAATSCHAPPELIJKE_BATEN"
            :indicator-lijst="
              getIndicatorLijst(IndicatorlijstNamen.MAATSCHAPPELIJKE_BATEN)
            "
          />
          <template
            v-if="
              !getIndicatorLijst(IndicatorlijstNamen.MAATSCHAPPELIJKE_BATEN)
            "
            >{{ dataMissingLabel }}</template
          >
        </RidCol>
      </RidRow>
      <RidRow>
        <ProjectSingleKosten
          v-if="project"
          :start-datum="startDatum"
          :project="project"
        />
      </RidRow>
      <RidRow>
        <RidCol id="documentatie" title="Documentatie" :title-in-bar="true">
          <IndicatorLijstExpansion
            v-if="project"
            :indicator-lijst-namen="indicatorlijstNamenDocumentatie"
            :project="project"
          />
        </RidCol>
      </RidRow>
      <RidRow>
        <Werkwijze
          v-if="project"
          :indicator-lijst-algemeen="
            getIndicatorLijst(IndicatorlijstNamen.ALGEMEEN)
          "
          :indicator-lijst-marktpartijen="
            getIndicatorLijst(IndicatorlijstNamen.ONTWIKKELPARTIJEN)
          "
          :project="project"
        />
      </RidRow>

      <ProjectManyTiles
        v-for="o in onderwerpen"
        :key="o"
        :filters="[{ attribute: 'Onderwerp', values: [o] }]"
        :current-project-id="project?.ProjectId"
        :title="`Andere activiteiten met onderwerp '${o.toLowerCase()}'`"
      />
    </template>
  </Page>
</template>

<script setup lang="ts">
import Page from "@/components/Page.vue"
import IndicatorLijstTabel from "./IndicatorLijstTabel/IndicatorLijstTabel.vue"
import type {
  ProjectMetAlleMetricsEnIndicatorLijsten,
  IndicatorLijst,
} from "@/api-new"
import { IndicatorlijstNamen } from "@/api-new"
import type { Formulier } from "@/api-new"
import { sortArrayByKey } from "@/util"
import { getOne, projectSpreadsheetUrl } from "@/services/project"
import { deepClone } from "@/util"
import FormattedValue from "@/components/FormattedValue.vue"
import ProjectSingleKosten from "./ProjectSingleKosten.vue"
import { useGlobalStore } from "@/store/useGlobalStore"
import RidCol from "@/components/RidCol.vue"
import Werkwijze from "./ProjectSingle/Werkwijze.vue"
import IndicatorLijstExpansion from "./IndicatorLijstTabel/IndicatorLijstExpansion.vue"
import ProjectManyTiles from "@/views/Project/ProjectManyTiles.vue"
import RidRow from "@/components/RidRow.vue"
import { useRouteQuery } from "@vueuse/router"
import { useIndicatorLijst } from "@/composables/useIndicatorLijst"
import IndicatorLijstButton from "./IndicatorLijstTabel/IndicatorLijstButton.vue"
import RidButton from "@/components/RidButton.vue"
import RidDialog from "@/components/RidDialog.vue"
import DropdownVanilla from "@/components/DropdownVanilla.vue"

const { state, contentOnly } = useGlobalStore()

const props = defineProps<{
  projectId?: string
  legacyProjectId?: string
}>()
const { projectId } = toRefs(props)

const tab = ref<IndicatorlijstNamen | null>(null)

const project = ref<ProjectMetAlleMetricsEnIndicatorLijsten | null>(null)
const errorMessage = ref<string | undefined>(undefined)

const tabs = computed(() => {
  const sortedIndicatorLijsten = (
    project.value?.IndicatorLijstWaardesGecorrigeerd
      ? sortArrayByKey(
          project.value.IndicatorLijstWaardesGecorrigeerd,
          "IndicatorLijstIndex",
        )
      : []
  ) as IndicatorLijst[]
  return sortedIndicatorLijsten.map((iL) => iL.IndicatorLijstMeervoudsNaam)
})

const dataMissingLabel = "Niet ingevuld voor deze ICT-activiteit."

const loading = ref<boolean>(true)

const projectVersieIdQuery = useRouteQuery("projectVersieId")
const tokenQuery = useRouteQuery("token")

const projectVersieId = computed(() => {
  const value = projectVersieIdQuery.value as string
  return parseInt(value)
})

const getProject = async () => {
  loading.value = true
  state.loadingCurrentProject = true
  const token = tokenQuery.value as string
  const relevantProjectId = projectId.value || props.legacyProjectId
  if (relevantProjectId === undefined) throw new Error("No project id provided")
  const isLegacyProjectId = Boolean(props.legacyProjectId)
  const { data, error } = await getOne(
    relevantProjectId,
    !isNaN(projectVersieId.value) ? projectVersieId.value : undefined,
    token,
    isLegacyProjectId,
  )
  if (!error) {
    project.value = data
    state.loadingCurrentProject = false
    state.currentProject = project.value
    tab.value = tabs.value.length > 0 ? tabs.value[0] : null
    loading.value = false
  } else {
    errorMessage.value = error
  }
}

const { getIndicatorLijst } = useIndicatorLijst(project)

const aanleiding = computed(
  () =>
    getIndicatorLijst(
      IndicatorlijstNamen.ALGEMEEN,
    )?.Formulier[0].FormulierWaardes.find(
      (fW) => fW.IndicatorTitel == "Aanleiding",
    )?.Waarde || undefined,
)

const description = computed(() => {
  return aanleiding.value?.split("\n")[0]
})

const summary = computed((): Record<string, string | null | undefined> => {
  return {
    Aanleiding: aanleiding.value,
    Doelstelling: getIndicatorLijst(
      IndicatorlijstNamen.ALGEMEEN,
    )?.Formulier[0].FormulierWaardes.find(
      (fW) => fW.IndicatorTitel == "Doelstelling",
    )?.Waarde,
  }
})

const formulierAlgemeenExcludedIndicatoren = [
  "Organisatie",
  "Aanleiding",
  "Functiepunten",
  "Doelstelling",
  "Zelfstandig bestuursorgaan",
  "Toelichting",
  "Gepubliceerd op",
  "Maatwerk",
  "Ontwikkelwijze",
  "Interne bedrijfsvoering",
]

const formulierAlgemeenIndicatorenSequence = [
  "Ministerie",
  "Bewindspersoon",
  "Startdatum",
  "Projectfase",
  "Peildatum",
  "Onderwerp",
  "Maatschappelijk baat",
  "Organisatie",
  "Ontwikkelwijze",
  "Maatwerk",
  "Samenwerkende ministerie(s)",
  "Tekst",
]

// export project
enum ExportFormat {
  Excel = "Excel (.xlsx)",
  ODS = "OpenDocument Spreadsheet (.ods)",
}
const exportButton = ref<typeof RidButton | null>(null)
const showExportDialog = ref<boolean>(false)
const exportFormats = Object.values(ExportFormat)
const selectedExportFormat = ref<string>(exportFormats[0])
const selectFormat = ref<HTMLDivElement | null>(null)
watch(selectFormat, () => {
  if (selectFormat.value) {
    selectFormat.value.querySelector("select")?.focus()
  }
})

const formulierAlgemeen = computed(() => {
  // Manually add ministerie
  const indicatorLijst = getIndicatorLijst(IndicatorlijstNamen.ALGEMEEN)
  if (indicatorLijst) {
    const formulier = deepClone(indicatorLijst)?.Formulier as Formulier[]

    if (formulier && formulier.length > 0) {
      formulier[0].FormulierWaardes = [
        {
          IndicatorIndex: -1,
          IndicatorTitel: "Ministerie",
          Waarde: project.value?.MinisterieNaam || "",
          IndicatorAntwoordTypeNaam: "Tekst",
        },
        {
          IndicatorIndex: 0,
          IndicatorTitel: "Projectfase",
          Waarde: project.value?.ProjectStatus || "",
          IndicatorAntwoordTypeNaam: "Tekst",
        },
        {
          IndicatorIndex: 0,
          IndicatorTitel: "Organisatie",
          Waarde: project.value?.OrganisatieNaam || "",
          IndicatorAntwoordTypeNaam: "Tekst",
        },
        {
          IndicatorIndex: 0,
          IndicatorTitel: "Peildatum",
          Waarde: (project.value?.PeilDatum || "")
            .split("-")
            .reverse()
            .join("-"),
          IndicatorAntwoordTypeNaam: "Tekst",
        },
        {
          IndicatorIndex: 0,
          IndicatorTitel: "Dienstverlening",
          Waarde: project.value?.Dienstverlening || "",
          IndicatorAntwoordTypeNaam: "MeerKeuze",
        },

        {
          IndicatorIndex: 0,
          IndicatorTitel: "Heeft AcICT-advies gehad",
          Waarde: project.value?.HeeftAcICTAdvies || "",
          IndicatorAntwoordTypeNaam: "Tekst",
        },
        ...formulier[0].FormulierWaardes.filter(
          (fW) =>
            !formulierAlgemeenExcludedIndicatoren.includes(fW.IndicatorTitel),
        ),
      ]
    }

    return formulier
  } else {
    return null
  }
})

const startDatum = computed(() => {
  const indicatorlijstAlgemeen = getIndicatorLijst(IndicatorlijstNamen.ALGEMEEN)
  const firstFormulier = indicatorlijstAlgemeen?.Formulier[0]
  const startDatumString = firstFormulier?.FormulierWaardes.find(
    (fW) => fW.IndicatorTitel == "Startdatum",
  )?.Waarde
  return startDatumString ? new Date(startDatumString) : undefined
})

const onderwerpen = computed(() => {
  const indicatorlijstAlgemeen = getIndicatorLijst(IndicatorlijstNamen.ALGEMEEN)
  return (
    (
      indicatorlijstAlgemeen?.Formulier[0].FormulierWaardes.find(
        (fW) => fW.IndicatorTitel == "Onderwerp",
      )?.Waarde || ""
    ).split(";") || []
  ).filter((v) => v && v.length > 0) // filter out onderwerpen that are an empty string
})

const indicatorlijstNamenDocumentatie: IndicatorlijstNamen[] = [
  IndicatorlijstNamen.TWEEDE_KAMERSTUKKEN,
  IndicatorlijstNamen.KWALITEITSTOETSEN,
]

watch(projectId, () => getProject(), { immediate: true })
</script>

<style lang="scss" scoped>
@import "@/styles/_colors.scss";

.v-tab {
  text-transform: none !important;
  color: $hemelblauw;
}

.export {
  color: white;
}

img {
  width: 90%;
  margin: auto;
  display: block;
}

.v-card-text p {
  line-height: 1.4em;
}
.buttons {
  display: flex;
  justify-content: flex-end;
  // width: 100%;
}

.buttons button {
  margin-left: 1em;
}

.window {
  overflow-x: auto;
  overflow-y: auto;
}

.laatst-gewijzigd {
  color: $grijs6; // grijs6 heeft genoeg contrast met de witte achtergrond
}

.block {
  display: flex;
  min-width: 100%;
  min-height: 100%;
}

a:hover {
  text-decoration: none !important;
}

.button-full-height {
  height: 44px;
}
</style>
