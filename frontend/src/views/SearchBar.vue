<template>
  <div
    class="container"
    role="combobox"
    @focusin="handleFocusIn"
    @focusout="handleFocusOut"
  >
    <v-text-field-accessible
      ref="searchBar"
      v-model="searchQuery"
      :hide-details="true"
      label-and-placeholder="Zoeken"
      append-inner-icon="mdi-magnify"
      :loading="loading"
      flat
      aria-autocomplete="list"
      aria-controls="search-results"
      :aria-expanded="nResults > 0 ? 'true' : 'false'"
      :aria-activedescendant="
        selectedSearchResultIndex !== null
          ? `search-result-${selectedSearchResultIndex}`
          : ''
      "
      :class="[
        'ml-auto',
        {
          'w-collapsed': collapsed,
        },
      ]"
      @keydown.down="
        (e: any) => [e.preventDefault(), selectSearchResult('next')]
      "
      @keydown.up="
        (e: any) => [e.preventDefault(), selectSearchResult('previous')]
      "
      @keydown.enter="navigateToSearchResult()"
      @keydown.esc="showSearchResults = false"
    >
    </v-text-field-accessible>
    <div
      v-if="showSearchResults"
      id="search-results"
      ref="searchResultsElement"
      class="search-results"
      role="listbox"
      @mouseenter="focusedOnResults = true"
      @mouseleave="focusedOnResults = false"
    >
      <div
        v-if="nResults == 0 && showSearchResults && !loading && !awaitingInput"
        class="pl-3 search-result"
      >
        Geen resultaten gevonden voor <strong>{{ searchQuery }}</strong>
      </div>
      <template v-for="(k, categoryIndex) in searchResultCategories" :key="k">
        <ul :aria-label="`Categorie ${resultConfig[k].label}`">
          <template v-if="searchResults[k].length > 0">
            <h4 class="mb-0 pl-3">
              {{ resultConfig[k].label }} ({{
                (searchResults?.[k] || []).length
              }})
            </h4>

            <li
              v-for="(val, index) in (searchResults?.[k] || []).slice(
                0,
                maxSearchResults,
              )"
              :id="`search-result-${getSearchResultIndex(
                categoryIndex,
                index,
              )}`"
              :key="JSON.stringify(val)"
              :class="[
                'pl-3 search-result',
                selectedSearchResultIndex ==
                  getSearchResultIndex(categoryIndex, index) && 'selected',
              ]"
              tabindex="1"
              role="option"
              :aria-selected="
                getSearchResultIndex(categoryIndex, index) ==
                selectedSearchResultIndex
                  ? 'true'
                  : 'false'
              "
            >
              <router-link
                v-if="k != 'overig'"
                :to="getRoute(k, val)"
                @click="handleResultClick"
              >
                {{ val.title }}
              </router-link>

              <a v-else-if="val.url" :href="val.url">
                {{ val.title }}
              </a>
            </li>
            <div
              v-if="(searchResults?.[k] || []).length > maxSearchResults"
              class="pl-3"
            >
              <router-link :to="getRoute(k)">
                {{ (searchResults?.[k] || []).length - maxSearchResults }}
                {{
                  (searchResults?.[k] || []).length - maxSearchResults == 1
                    ? "overig resultaat"
                    : "overige resultaten"
                }}
              </router-link>
            </div>
          </template>
        </ul>
      </template>
    </div>
  </div>

  <ScreenreaderMessageLiveArea>{{
    screenreaderMessage
  }}</ScreenreaderMessageLiveArea>
</template>

<script setup lang="ts">
import VTextFieldAccessible from "@/components/VuetifyAccessible/vTextFieldAccessible.vue"
import { search } from "@/services/search"
import type { SearchResults, SearchResult } from "@/api-new"
import { watchDebounced } from "@vueuse/core"
import ScreenreaderMessageLiveArea from "@/components/ScreenreaderMessageLiveArea.vue"
import { useDisplay } from "vuetify"
import { getObjectKeys } from "@/util"

const props = defineProps<{
  applyCollapsing?: boolean
}>()

const { smAndDown } = useDisplay()
const collapsed = ref<boolean>(props.applyCollapsing && !smAndDown.value)
const focusedOnResults = ref<boolean>(false)

const searchQuery = ref<string>("")

const screenreaderMessage = ref<string>("")

const loading = ref<boolean>(false)
const awaitingInput = ref<boolean>(false)

const defaultResults = {
  projects: [],
  ministeries: [],
  onderwerpen: [],
  i_strategie: [],
  overig: [],
}
const searchResults = ref<SearchResults>(defaultResults)

type SearchResultMeta = {
  route: string
  label: string
  paramKey: string
}
const maxSearchResults = 5

const resultConfig: Record<keyof SearchResults, SearchResultMeta> = {
  projects: {
    route: "ict-activiteit",
    label: "Grote ICT-activiteiten",
    paramKey: "projectId",
  },
  ministeries: {
    route: "ministerie",
    label: "Ministeries",
    paramKey: "attributeValue",
  },
  onderwerpen: {
    route: "onderwerp",
    label: "Onderwerpen",
    paramKey: "attributeValue",
  },
  i_strategie: {
    route: "i-strategie",
    label: "I-strategie",
    paramKey: "attributeValue",
  },
  overig: {
    route: "overig",
    label: "Overig",
    paramKey: "attributeValue",
  },
}

const nResults = computed(() => {
  const searchResultKeys = getObjectKeys(searchResults.value)
  return searchResultKeys.reduce((count, key) => {
    return (count = count + searchResults.value[key].length)
  }, 0)
})

const searchResultCategories = computed(
  () => Object.keys(searchResults.value) as (keyof SearchResults)[],
)

async function getSearchResults() {
  loading.value = true
  searchResults.value = await search(searchQuery.value)
  loading.value = false
}

const showSearchResults = ref<boolean>(false)

watch(searchResults, () => {
  if (searchQuery.value) {
    screenreaderMessage.value = `${nResults.value} ${
      nResults.value == 1 ? "resultaat" : "resultaten"
    } gevonden voor zoekterm '${searchQuery.value}'.${
      nResults.value > 0
        ? " Navigeer met 'enter' naar de pagina van het zoekresultaat."
        : ""
    }`
    showSearchResults.value = true
  } else {
    showSearchResults.value = false
  }

  if (nResults.value === 0) {
    selectedSearchResultIndex.value = null
  }
})

watch(searchQuery, () => {
  // trigger loading variable with a normal watcher, because watchDebounced is delayed
  if (searchQuery.value.length > 0) {
    awaitingInput.value = true
    selectedSearchResultIndex.value = null
  } else {
    selectedSearchResultIndex.value = null
  }
})

watch(smAndDown, () => {
  if (
    props.applyCollapsing &&
    !smAndDown.value &&
    searchQuery.value.length == 0
  ) {
    collapsed.value = true
  } else if (smAndDown.value) {
    collapsed.value = false
  }
})

watchDebounced(
  searchQuery,
  async () => {
    if (searchQuery.value.length > 0) {
      await getSearchResults()
      awaitingInput.value = false
    } else {
      searchResults.value = defaultResults
    }
  },
  { debounce: 400 },
)

function getRoute(key: keyof SearchResults, v?: SearchResult) {
  const routeName = resultConfig[key].route
  const routeLabel = resultConfig[key].label

  if (key == "overig" && v) {
    return {
      path: v.url,
    }
  }

  if (!v) {
    return {
      name: "zoekresultaten",
      query: {
        searchType: key,
        searchQuery: searchQuery.value,
        category: routeLabel,
      },
    }
  }
  const idValue = v.id
  const routeParamKey = resultConfig[key].paramKey
  const route = {
    name: routeName,
    params: { [routeParamKey]: idValue },
  }
  return route
}

const selectedSearchResultIndex = ref<number | null>(null)
const selectedSearchResult = computed(() => {
  const results = searchResultCategories.value.reduce(
    (arr: SearchResult[], category) => {
      const categoryResults = searchResults.value[category].slice(
        0,
        maxSearchResults,
      ) as SearchResult[]
      return [...arr, ...categoryResults]
    },
    [],
  )

  if (selectedSearchResultIndex.value !== null) {
    return results[selectedSearchResultIndex.value]
  } else {
    return null
  }
})

const searchResultCategoryWithLength = computed(() =>
  searchResultCategories.value.reduce(
    (resultWithLength: Record<string, number>, category) => {
      resultWithLength[category] =
        maxSearchResults > searchResults.value[category].length
          ? searchResults.value[category].length
          : maxSearchResults

      return resultWithLength
    },
    {},
  ),
)

function handleResultClick() {
  focusedOnResults.value = false
  handleFocusOut()
}

function handleFocusIn() {
  if (collapsed.value) {
    collapsed.value = false
  } else if (searchQuery.value) {
    showSearchResults.value = true
  }
}

function handleFocusOut() {
  if (
    props.applyCollapsing &&
    searchQuery.value == "" &&
    !smAndDown.value &&
    !focusedOnResults.value
  ) {
    collapsed.value = true
    showSearchResults.value = false
  } else if (searchQuery.value.length > 0 && !focusedOnResults.value) {
    showSearchResults.value = false
  }
}

function getSearchResultIndex(categoryIndex: number, index: number) {
  let previousLengths = 0
  for (let index = 0; index < categoryIndex; index++) {
    const category = searchResultCategories.value[index]
    const categoryResults = searchResults.value[category]
    previousLengths =
      previousLengths +
      (maxSearchResults > categoryResults.length
        ? categoryResults.length
        : maxSearchResults)
  }
  return previousLengths + index
}

function selectSearchResult(direction: "next" | "previous") {
  const delta = direction == "next" ? 1 : -1

  const totalVisibleSearchResultCount = searchResultCategories.value.reduce(
    (total, category) => {
      const categoryResults = searchResults.value[category]
      return (
        total +
        (maxSearchResults > categoryResults.length
          ? categoryResults.length
          : maxSearchResults)
      )
    },
    0,
  )

  const allowSelectionChange =
    (direction == "next" &&
      selectedSearchResultIndex.value &&
      selectedSearchResultIndex.value < totalVisibleSearchResultCount - 1) ||
    (direction == "previous" &&
      selectedSearchResultIndex.value &&
      selectedSearchResultIndex.value > 0) ||
    (direction == "next" &&
      !selectedSearchResultIndex.value &&
      nResults.value > 0)

  if (allowSelectionChange) {
    selectedSearchResultIndex.value =
      (selectedSearchResultIndex.value === null
        ? -1
        : selectedSearchResultIndex.value) + delta
  }

  const element = document.getElementById(
    `search-result-${selectedSearchResultIndex.value}`,
  )
  if (element)
    element.scrollIntoView({
      behavior: "smooth",
      block: "nearest",
    })
}

const router = useRouter()

function navigateToSearchResult() {
  const searchResult = selectedSearchResult.value
  if (!searchResult) {
    throw new Error("No search result selected")
  }

  const categoryLengths = searchResultCategories.value.map(
    (c) => searchResultCategoryWithLength.value[c],
  )

  const cumulativeSum = (
    (sum: number) => (value: number) =>
      (sum += value)
  )(0)

  const cumulativeLengths = categoryLengths.map(cumulativeSum)

  // find the category index in the cumulative length array
  const categoryIndex = cumulativeLengths.findIndex(
    (currentLength) => (selectedSearchResultIndex.value || 0) < currentLength,
  )

  const category = searchResultCategories.value[
    categoryIndex
  ] as keyof SearchResults

  const route = getRoute(category, searchResult)
  if (category != "overig") {
    router.push(route)
  } else if (searchResult.url) {
    window.location.href = searchResult.url
  }
}
</script>

<style scoped lang="scss">
@import "@/styles/_colors.scss";

.search-results {
  max-height: 300px; /* Set the maximum height for the search results container */
  overflow-y: auto; /* Add a scrollbar when the results exceed the container height */
  background-color: white;
  width: 100%;
  position: absolute;
  z-index: 1;
  border: 1px solid black;
  padding-top: 0.5em;
}

.search-results,
.search-results h4 {
  font-size: 0.9em;
}

.search-field {
  background-color: white;
}

.search-results li {
  padding: 0.3em 0 0.3em 0;
  cursor: pointer;
}

.search-results div:hover,
.search-results .selected {
  background-color: $tertiary;
  text-decoration: none;
}

.container {
  width: 100%;
  position: relative;
}

.w-collapsed {
  width: 13%;
}
</style>
