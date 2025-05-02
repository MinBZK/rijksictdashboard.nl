<template>
  <Page title="Zoekresultaten" :subtitle="subtitle">
    <Pagination
      v-if="numberOfResults > pageLength"
      v-model:page="state.page"
      :total-count="numberOfResults"
      :page-length="pageLength"
      :n-pages="nPages"
      class="justify-end"
      @update-page="setPage"
    />
    <ul class="pl-5">
      <li v-for="result in paginatedResults" :key="result.id" class="mb-2">
        <component
          :is="result.url ? 'a' : 'router-link'"
          :href="result.url ? result.url : undefined"
          :to="result.url ? undefined : getRoute(key, result)"
          class="cursor-pointer"
        >
          {{ result.title }} </component
        ><br />
        <span
          v-if="result.content_element && result.matched_elements"
          v-html="
            highlightContent(result.content_element, result.matched_elements)
          "
        ></span>
      </li>
    </ul>
  </Page>
</template>

<script setup lang="ts">
import Page from "@/components/Page.vue"
import type { SearchResult, SearchResults } from "@/api-new"
import { search } from "@/services/search"
import Pagination from "@/components/Pagination.vue"
import type { SearchResultMeta } from "@/types/search"

const route = useRoute()
const router = useRouter()

const props = defineProps<{
  searchType: keyof SearchResults
  searchQuery: string
  category: string
}>()

const key = ref<keyof SearchResults>(
  (route.query.searchType || props.searchType) as keyof SearchResults,
)
const searchQuery = ref<string>(
  route.query.searchQuery?.toString() || props.searchQuery || "",
)
const category = ref<string>(
  route.query.category?.toString() || props.category || "",
)
const results = ref<SearchResult[]>([])

const state = reactive({
  page: Number(route.query.page) || 1,
})

const resultConfig: Record<keyof SearchResults, SearchResultMeta> = {
  projects: {
    route: "ict-activiteit",
    paramKey: "projectId",
  },
  ministeries: {
    route: "ministerie",
    paramKey: "attributeValue",
  },
  onderwerpen: {
    route: "onderwerp",
    paramKey: "attributeValue",
  },
  i_strategie: {
    route: "i-strategie",
    paramKey: "attributeValue",
  },
  overig: {
    route: "overig",
    paramKey: "attributeValue",
  },
}

const numberOfResults = computed(() => results?.value.length || 0)

const pageLength = 20
const startIndex = computed(() => (state.page - 1) * pageLength + 1)
const endIndex = computed(() => {
  const isLastPage = state.page === nPages.value
  const lastPageLength = numberOfResults.value % pageLength || pageLength
  return isLastPage
    ? startIndex.value + lastPageLength - 1
    : startIndex.value + pageLength - 1
})
const nPages = computed(() => Math.ceil(numberOfResults.value / pageLength))

const paginatedResults = computed(() => {
  return results.value.slice(startIndex.value - 1, endIndex.value)
})
const subtitle = computed(() => {
  return `${numberOfResults.value} resultaten gevonden voor '${searchQuery.value}' in ${category.value}`
})

async function getSearchResults() {
  results.value = (await search(searchQuery.value, key.value))[key.value]
}
getSearchResults()

function highlightContent(content: string, matchedElements: string[]): string {
  if (!matchedElements) return content

  const sentences = content.match(/[^.!?]+[.!?]+/g) || [content]

  const highlightedSentences = sentences.map((sentence) => {
    const words = sentence.split(" ")
    const highlightedWords = words.map((word) => {
      if (matchedElements.includes(word)) {
        return `<strong>${word}</strong>`
      }
      return word
    })
    return highlightedWords.join(" ")
  })
  const filteredSentences = highlightedSentences.filter((sentence) =>
    matchedElements.some((word) =>
      sentence.includes(`<strong>${word}</strong>`),
    ),
  )
  const highlightedContent = filteredSentences.join(" ")

  const highlightedContentWords = content.split(" ")
  if (highlightedContentWords.length > 30) {
    return highlightedContentWords.slice(0, 30).join(" ") + "..."
  }

  return highlightedContent
}

function getRoute(key: keyof SearchResults, v: SearchResult) {
  const routeName = resultConfig[key].route
  const idValue = v.id
  const routeParamKey = resultConfig[key].paramKey
  const route = {
    name: routeName,
    params: { [routeParamKey]: idValue },
  }
  return route
}

const setPage = (pageNumber: number) => {
  state.page = pageNumber
  router.push({
    name: "zoekresultaten",
    query: {
      key: key.value,
      category: category.value,
      searchQuery: searchQuery.value,
      page: pageNumber,
    },
  })
}
</script>
