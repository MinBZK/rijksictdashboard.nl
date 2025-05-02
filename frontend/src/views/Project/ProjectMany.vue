<template>
  <Page
    title="Overzicht van grote ICT-activiteiten"
    :show-drawer="showDrawer"
    @close-drawer="showDrawer = false"
  >
    <div class="mb-5 description">
      <span v-html="getContent('Grote ICT-activiteiten', 'preview').value" />
    </div>

    <div class="mb-5 description">
      <span
        v-html="getContent('ICT-activiteiten overzicht', 'content').value"
      />
    </div>

    <v-row>
      <v-col cols="12" :md="6">
        <!-- <v-text-field /> -->
        <ScreenreaderMessageLiveArea>{{
          screenreaderMessage
        }}</ScreenreaderMessageLiveArea>
        <v-text-field-accessible
          v-model="searchQueryInternal"
          variant="outlined"
          flat
          clearable
          label-and-placeholder="Filter het ICT-activiteiten overzicht op naam door in dit invoerveld te typen."
          :is-search-bar="true"
      /></v-col>
    </v-row>

    <ScreenreaderHeading
      title="Filters"
      heading-level="2"
      :description="`Filters kunnen worden toegepast middels keuzelijsten. Sluit keuzelijst middels tweemaal 'escape', wissel van keuzelijst met 'tab', selecteer waarde in keuzelijst middels pijltjestoets.`"
    />
    <RidRow
      :small-title="true"
      :no-bottom-padding="true"
      :allow-hide="true"
      align-toggle-label="left"
      show-more-label="Toon filters"
      show-less-label="Verberg filters"
      title="Filters"
      :title-screenreader-only="true"
    >
      <v-col
        v-for="{ aggregation_attribute, values } in projectAggregations"
        :key="aggregation_attribute"
        :cols="12"
        :sm="6"
        :md="4"
      >
        <ProjectFilterSelect
          :attribute="aggregation_attribute as keyof DisplayedAttributes"
          :values="values"
          :column-name="
            displayedAttributes[
              aggregation_attribute as keyof DisplayedAttributes
            ].label
          "
          :filters="
            state.filters.find((aF) => aF.attribute == aggregation_attribute)
          "
          @update="
            (values) =>
              updateFilter(values, aggregation_attribute as ProjectAttribute)
          "
        />
      </v-col>
    </RidRow>
    <v-row>
      <v-col class="pb-0">
        <template
          v-for="f in [...orderedFilters, ...undefinedFilters]"
          :key="f.attribute"
        >
          <v-chip
            v-for="v in f?.values || []"
            :key="v"
            class="mr-3 mb-3"
            :color="getDisplayedAttribute(f.attribute)?.chipColor || 'grijs7'"
            :aria-label="`Verwijder filter ${
              getDisplayedAttribute(f.attribute)?.label || f.attribute
            } = ${v || '(niet ingevuld)'}`"
            closable
            size="large"
            role="button"
            tabindex="0"
            @keyup.enter="removeFilterValue(f.attribute, v)"
            @click="removeFilterValue(f.attribute, v)"
          >
            {{ getDisplayedAttribute(f.attribute)?.label || f.attribute }}:
            {{ v || "(niet ingevuld)" }}</v-chip
          >
        </template>
      </v-col>
    </v-row>

    <ScreenreaderHeading
      title="Overzicht van grote ICT-activiteiten"
      description="Overzicht is in tabelvorm en bevat één of meerdere pagina's"
      heading-level="2"
    />

    <v-row class="mb-4">
      <v-col :cols="smAndDown ? 12 : 6">
        <RidButton
          v-if="hasFilterOrSorting"
          prepend-icon="mdi-close"
          @click="mutations.resetFiltersAndSorting"
          @keyup.enter="mutations.resetFiltersAndSorting"
          >Verwijder alle filters en sortering</RidButton
        >
      </v-col>
      <v-col :cols="smAndDown ? 12 : 6" class="d-flex justify-end">
        <Pagination
          title="ICT-activiteit"
          :total-count="totalCount"
          :v-model:page="page"
          :page-length="pageLength"
          :n-pages="nPages"
          @update-page="mutations.setPage"
        />
      </v-col>
    </v-row>
    <v-table>
      <colgroup>
        <col
          v-for="index in nColumns"
          :key="index"
          :span="index"
          :width="`${parseInt((100 / nColumns).toString())}%`"
        />
      </colgroup>
      <thead>
        <tr>
          <th
            v-for="attributeKey in displayedAttributeKeys"
            :key="attributeKey"
            scope="column"
          >
            {{ displayedAttributes[attributeKey].label }}
            <span
              role="button"
              tabindex="0"
              :aria-label="getSortingIcon(attributeKey).label"
              :title="getSortingIcon(attributeKey).label"
              class="icon-button"
              :class="{
                disabled: loading,
                'has-sorting':
                  state.sorting.filter((aS) => aS.attribute == attributeKey)
                    .length > 0,
              }"
              @click="!loading ? toggleSorting(attributeKey) : null"
              @keydown.space="!loading ? toggleSorting(attributeKey) : null"
              @keydown.enter="!loading ? toggleSorting(attributeKey) : null"
              ><v-icon :icon="getSortingIcon(attributeKey).icon"
            /></span>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr class="row-loading">
          <td :colspan="nColumns">
            <v-progress-linear
              v-if="loading && projecten.length > 0"
              role="progressbar"
              aria-label="progressiebar"
              indeterminate
              color="primary"
            ></v-progress-linear>
          </td>
        </tr>

        <tr v-for="project in projecten" :key="project.ProjectId">
          <td v-for="attribute in displayedAttributeKeys" :key="attribute">
            <template v-if="attribute == 'SoortICTActiviteit'">
              <router-link
                v-if="project[attribute]"
                :class="`px-4 py-1 text-white ${getBackgroundColor(project[attribute]!)}`"
                :to="{
                  name: 'soort',
                  params: { attributeValue: project[attribute] },
                }"
              >
                <ProjectValue
                  :data-type="'string'"
                  :value="project[attribute]!"
                />
              </router-link>
            </template>
            <template v-else-if="attribute == 'Naam'"
              ><router-link
                :to="{
                  name: 'ict-activiteit',
                  params: { projectId: project.ProjectId, slug: project.Slug },
                }"
              >
                <ProjectValue :data-type="'string'" :value="project[attribute]"
              /></router-link>
            </template>
            <template v-else-if="attribute == 'MinisterieNaam'"
              ><router-link
                :to="{
                  name: 'ministerie',
                  params: { attributeValue: project[attribute] },
                }"
              >
                <ProjectValue :data-type="'string'" :value="project[attribute]"
              /></router-link>
            </template>

            <template v-else-if="attribute == 'Onderwerp'">
              <span
                v-if="splitListValue(attribute, project).length == 0"
                class="sr-only"
                >Geen waarde</span
              >
              <ul>
                <li
                  v-for="splittedValue in splitListValue(attribute, project)"
                  :key="splittedValue"
                >
                  <router-link
                    v-if="splittedValue"
                    :to="{
                      name: 'onderwerp',
                      params: { attributeValue: splittedValue },
                    }"
                  >
                    <ProjectValue
                      :data-type="'string'"
                      :value="splittedValue"
                    />
                  </router-link>
                </li>
              </ul>
            </template>

            <!--ts-ignore-->
            <template
              v-else-if="
                //@ts-ignore
                project[attribute]
              "
            >
              <FormattedValue
                :format-config="displayedAttributes[attribute].formatConfig"
                :value="project[attribute]"
              />
            </template>
            <template v-else>
              <span class="ml-1">-</span>
            </template>
          </td>
        </tr>

        <tr v-if="projecten.length == 0">
          <td :colspan="nColumns" class="text-center">
            <template v-if="initialized"
              >Geen grote ICT-activiteiten gevonden, pas zoekopdracht aan. </template
            ><template v-else>
              <SpinnerVue />
            </template>
          </td>
        </tr>
      </tbody>
    </v-table>
    <v-row class="flex justify-center">
      <v-col :cols="smAndDown ? 12 : 6">
        <Pagination
          title="ICT-activiteit"
          :total-count="totalCount"
          :state="state"
          :n-pages="nPages"
          :page-length="pageLength"
          :scroll-to-top="true"
          :top-offset="550"
          @update-page="mutations.setPage"
        />
      </v-col>
    </v-row>
  </Page>
</template>

<script setup lang="ts">
import Page from "@/components/Page.vue"
import ProjectValue from "@/views/Project/ProjectAttributeValue.vue"
import { useRouter } from "vue-router"
import SpinnerVue from "@/components/Spinner.vue"
import { useProjecten } from "@/composables/useProjecten"
import FormattedValue from "@/components/FormattedValue.vue"
import VTextFieldAccessible from "@/components/VuetifyAccessible/vTextFieldAccessible.vue"
import ProjectFilterSelect from "./ProjectFilterSelect.vue"
import RidRow from "@/components/RidRow.vue"
import type { AttributeSorting, ProjectFilter } from "@/types/project"
import RidButton from "@/components/RidButton.vue"
import { stringifyArray } from "@/util/querystring"
import { getObjectKeys, type FormatConfig } from "@/util"
import type { ProjectAttribute } from "@/types/project"
import type { ProjectMetAlleMetricsEnIndicatorLijsten } from "@/api-new"
import { useTextLoader } from "@/composables/useTextLoader"
import { useDisplay } from "vuetify"
import ScreenreaderMessageLiveArea from "@/components/ScreenreaderMessageLiveArea.vue"
import ScreenreaderHeading from "@/components/ScreenreaderHeading.vue"
import type { ProjectMetCoreMetrics } from "@/api-new"
import Pagination from "@/components/Pagination.vue"
import type { Colors } from "@/types/colors"

const { smAndDown } = useDisplay()

const { getContent } = useTextLoader()

const orderedFilters = computed(
  () =>
    state.aggregationAttributes
      .map((a) => state.filters.find((f) => f.attribute == a))
      .filter((pA) => pA) as ProjectFilter[],
)

// Undefined filters are not defined in the component. However, filters can be set on any attribute through the URL (for example by clicking through from other components)
const undefinedFilters = computed(() =>
  state.filters.filter(
    (f) =>
      !orderedFilters.value.map((oF) => oF.attribute).includes(f.attribute),
  ),
)

type ProjectProps = {
  page?: number
  filters?: ProjectFilter[]
  sorting?: AttributeSorting[]
  search?: string
  aggregationAttributes?: ProjectAttribute[]
}

const props = withDefaults(defineProps<ProjectProps>(), {
  page: 1,
  search: "",
  filters: (): ProjectFilter[] => [],
  sorting: (): AttributeSorting[] => [],
  aggregation_attributes: (): ProjectAttribute[] => [],
})

const defaultSorting: AttributeSorting[] = [
  {
    attribute: "MinisterieNaam",
    direction: "asc",
  },
]

const usedSorting = computed(() => {
  if (props.sorting.length == 0) {
    return defaultSorting
  } else {
    return props.sorting
  }
})

const searchQueryInternal = ref<string>(props.search)

interface ProjectManyState extends Omit<Required<ProjectProps>, "sorting"> {
  sorting: AttributeSorting[]
}

const filters = toRef(props, "filters")

const state: ProjectManyState = reactive({
  page: toRef(props, "page"),
  filters: filters,
  sorting: usedSorting,
  search: searchQueryInternal,
  aggregationAttributes: [
    "SoortICTActiviteit",
    "MinisterieNaam",
    "OrganisatieNaam",
    "Onderwerp",
    "ProjectStatus",
    "HeeftAcICTAdvies",
    "MaatschappelijkeBaat",
  ],
})

// pagina
const router = useRouter()
const showDrawer = ref<boolean>(false)

const mutations = {
  setPage: (page: number) => updateStateUrl({ page }),
  removeAllFilters: () =>
    updateStateUrl({
      filters: [],
      sorting: [],
      page: 1,
    }),
  resetFiltersAndSorting: () =>
    updateStateUrl({
      filters: [],
      sorting: [],
    }),
}

const nColumns = computed(() => displayedAttributeKeys.length)

const hasFilterOrSorting = computed(
  () => (props.sorting && props.sorting.length > 0) || state.filters.length > 0,
)

watch(searchQueryInternal, () => {
  updateStateUrl({ search: searchQueryInternal.value, page: 1 })
})

const toggleSorting = (attribute: ProjectAttribute) => {
  // copy sorting array, it will be later pushed to the route query
  let sorting = JSON.parse(JSON.stringify(state.sorting)) as AttributeSorting[]

  const currentSorting = sorting.find((aS) => aS.attribute == attribute)

  if (currentSorting?.direction == "asc") {
    // if attribute has no ascending sorting, apply descending sorting
    currentSorting.direction = "desc"
  } else if (currentSorting?.direction == "desc") {
    // if attribute has no descending sorting, remove sorting
    // const currentSortingIndex = state.sorting.indexOf(currentSorting)
    // state.sorting.splice(currentSortingIndex, 1)
    // currentSorting.ascending = true
    sorting = [...defaultSorting]
  } else {
    // if sorting is new, first clear existing list to ensure only sorting one at a time
    sorting = []
    // if attribute has no sorting yet, apply ascending sorting
    sorting.push({
      attribute,
      direction: "asc",
    })
  }

  // update route, which is a prop for this component, the prop is watched and will mutate the sorting ref
  updateStateUrl({
    sorting,
  })
}

const removeFilterValue = (attribute: ProjectAttribute, value: string) => {
  const filters = JSON.parse(JSON.stringify(state.filters)) as ProjectFilter[]
  const existingFilter = filters.find((aF) => aF.attribute == attribute)

  if (existingFilter) {
    const valueIndex = existingFilter.values.indexOf(value)
    existingFilter.values.splice(valueIndex, 1)
  }
  updateStateUrl({
    filters: filters.filter((f) => f.values.length > 0),
    page: 1,
  })
}

const updateFilter = (
  values: string[],
  aggregation_attribute: ProjectAttribute,
) => {
  const filters = JSON.parse(JSON.stringify(state.filters)) as ProjectFilter[]

  const existingFilter = filters.find(
    (aF) => aF.attribute == aggregation_attribute,
  )

  if (existingFilter && values.length == 0) {
    existingFilter.values = []
  } else if (existingFilter && values.length > 0) {
    existingFilter.values = values
  } else if (values.length > 0) {
    filters.push({
      attribute: aggregation_attribute,
      values: values,
    })
  }

  updateStateUrl({
    filters: filters.filter((f) => f.values.length > 0),
    page: 1,
  })
}

const colorCache: Record<string, string> = {}
const nextColorIndex = ref<number>(0)
function getBackgroundColor(value: string): string {
  const colors = [
    "bg-primary",
    "bg-violet",
    "bg-groen",
    "bg-oranje",
    "bg-paars",
    "bg-robijnrood",
    "bg-donkerbruin",
  ]
  if (colorCache[value]) return colorCache[value]

  const assignedColor = colors[nextColorIndex.value]
  colorCache[value] = assignedColor

  nextColorIndex.value = (nextColorIndex.value + 1) % colors.length

  return assignedColor
}

type DisplayedAttributes = Pick<
  ProjectMetAlleMetricsEnIndicatorLijsten,
  | "Naam"
  | "MinisterieNaam"
  | "OrganisatieNaam"
  | "Onderwerp"
  | "ProjectStatus"
  | "MaatschappelijkeBaat"
  | "SoortICTActiviteit"
  | "HeeftAcICTAdvies"
  | "SchattingEinddatumActueel"
>

type DisplayedAttributeConfig = {
  label: string
  chipColor?: Colors
  formatConfig: FormatConfig
  hideInTable?: boolean
  // unitSuffix?: string
  // maxDigits?: number
}

type DisplayedAttributeKey = keyof DisplayedAttributes

const displayedAttributes: {
  [K in DisplayedAttributeKey]: DisplayedAttributeConfig
} = {
  SoortICTActiviteit: {
    label: "Soort ICT-activiteit",
    formatConfig: {
      dataType: "string",
    },
    chipColor: "robijnrood",
  },
  Naam: {
    label: "Naam",
    formatConfig: {
      dataType: "string",
    },
  },
  MinisterieNaam: {
    label: "Ministerie",
    chipColor: "primary",
    formatConfig: {
      dataType: "string",
    },
  },
  OrganisatieNaam: {
    label: "Organisatie",
    chipColor: "hemelblauw",
    hideInTable: true,
    formatConfig: {
      dataType: "string",
    },
  },
  Onderwerp: {
    label: "Onderwerp",
    formatConfig: {
      dataType: "string",
    },
    chipColor: "groen",
  },
  ProjectStatus: {
    label: "Projectfase",
    formatConfig: {
      dataType: "string",
    },
    chipColor: "oranje",
    hideInTable: true,
  },
  HeeftAcICTAdvies: {
    label: "Heeft AcICT-advies gehad",
    formatConfig: {
      dataType: "string",
    },
    chipColor: "paars",
    hideInTable: true,
  },
  MaatschappelijkeBaat: {
    label: "Verbetert op",
    formatConfig: {
      dataType: "string",
    },
    chipColor: "donkerbruin",
    hideInTable: true,
  },
  SchattingEinddatumActueel: {
    label: "Verwachte einddatum",
    formatConfig: {
      dataType: "date",
    },
  },
}

const displayedAttributeKeys = getObjectKeys(displayedAttributes).filter(
  (key) =>
    displayedAttributes[key].hideInTable == undefined ||
    displayedAttributes[key].hideInTable == false,
)

const getSortingIcon = (attribute: string) => {
  const sortingStatus = state.sorting.find((aS) => aS.attribute == attribute)

  //@ts-expect-error
  const attributeLabel = displayedAttributes[attribute].label

  if (!sortingStatus) {
    return {
      icon: "mdi-menu-swap",
      label: `Sorteer op ${attributeLabel} oplopend`,
    }
  } else if (sortingStatus?.direction === "asc") {
    return {
      icon: "mdi-menu-up",
      label: `Sorteer op ${attributeLabel} aflopend`,
    }
  } else {
    return {
      icon: "mdi-menu-down",
      label: `Verwijder sortering op ${attributeLabel}`,
    }
  }
}

const {
  loading,
  initialized,
  pageLength,
  nPages,
  projecten,
  projectAggregations,
  totalCount,
} = useProjecten({
  state,
})

// watch(projecten, () => {
//   if (searchQueryInternal.value) {
//     screenreaderMessage.value = `Er ${nProjecten.value == 1 ? "is" : "zijn"} ${
//       nProjecten.value
//     } ${
//       nProjecten.value == 1 ? "activiteit" : "activiteiten"
//     } gevonden voor de zoekterm '${searchQueryInternal.value}'`
//   }
// })

const setScreenreaderMessage = () => {
  const suffixSearch = searchQueryInternal.value
    ? ` voor de zoekterm '${searchQueryInternal.value}'`
    : ""

  const filterColumnLabels = state.filters.map(
    //@ts-expect-error
    (f) => displayedAttributes[f.attribute].label,
  )

  const suffixFilters =
    filterColumnLabels.length > 0
      ? ` met ${
          filterColumnLabels.length == 1 ? "filter" : "filters"
        } voor '${filterColumnLabels.map((l) => l.toLowerCase()).join(", ")}'`
      : ""

  const message = `Er ${totalCount.value == 1 ? "is" : "zijn"} ${
    totalCount.value
  } ${
    totalCount.value == 1 ? "activiteit" : "activiteiten"
  } gevonden${suffixSearch}${suffixFilters}.`
  screenreaderMessage.value = message
}

const screenreaderMessage = ref<string>("")
watch(totalCount, () => setScreenreaderMessage())
const updateStateUrl = (updateQuery: ProjectProps) => {
  const {
    page = state.page,
    filters = state.filters,
    sorting = state.sorting,
    search = state.search,
  } = updateQuery

  const sortingIsDefault =
    JSON.stringify(sorting) == JSON.stringify(defaultSorting)

  router.push({
    name: "ICT-activiteiten",
    query: {
      page,
      filters: stringifyArray(filters, "filters"),
      // default sorting should not be stored in URL
      sorting: sortingIsDefault
        ? undefined
        : stringifyArray(sorting, "sorting"),
      search,
    },
  })
}

function splitListValue(
  attribute: DisplayedAttributeKey,
  project: ProjectMetCoreMetrics,
) {
  const list: string[] = (project[attribute] || "")
    .toString()
    .split(";")
    .filter((v: string) => v.length > 0)
  return list
}

const getDisplayedAttribute = (attribute: string) =>
  //@ts-expect-error
  displayedAttributes[attribute]
</script>

<style scoped lang="scss">
@import "@/styles/_colors.scss";

button {
  margin-right: 10px;
}

tbody tr:first-child td {
  padding: 0 !important;
  height: 4px !important;
  border-bottom: 0 !important;
}

.icon-button {
  color: $grijs6;
  font-size: 1em;
}

.icon-button:hover {
  color: $hemelblauw;
}

.icon-button.disabled {
  cursor: not-allowed;
  color: $grijs2;
}

.icon-button.has-sorting {
  color: $hemelblauw;
}

ul {
  list-style-type: none;
}

.description {
  max-width: 800px;
}
</style>
