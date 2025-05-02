import { getMany } from "@/services/project"

import type {
  ProjectFilter,
  AttributeSorting,
  ProjectAttribute,
} from "@/types/project"
import { watchDebounced } from "@vueuse/core"
import type {
  ProjectMetCoreMetrics,
  ProjectAttributeAggregation,
} from "@/api-new"

export type ProjectProps = {
  page?: number
  filters?: ProjectFilter[]
  sorting?: AttributeSorting[]
  aggregationAttributes?: ProjectAttribute[]
  search?: string
  limit?: number
}

export type ProjectQuery = {
  getDataWithoutQuery?: boolean
  state: ProjectProps
}

export const useProjecten = (query: ProjectQuery) => {
  const defaultState: ProjectProps = reactive({
    page: 1,
    filters: [],
    sorting: [],
    aggregationAttributes: [],
    search: "",
  })

  const { getDataWithoutQuery = true, state } = query

  Object.keys(state).map((stateKey) => {
    //@ts-expect-error
    if (!state[stateKey]) {
      //@ts-expect-error
      state[stateKey] = defaultState[stateKey]
    }
  })

  const loading = ref<boolean>(false)
  const searchQueryFinished = ref<boolean>(false)
  const initialized = ref<boolean>(false)
  const pageLength = state.limit || 20
  const nPages = computed(() => Math.ceil(totalCount.value / pageLength))
  const projecten = ref<ProjectMetCoreMetrics[]>([])
  const totalCount = ref<number>(0)
  const projectAggregations = ref<ProjectAttributeAggregation[]>([])

  const getData = async () => {
    loading.value = true
    const request = {
      page: state.page,
      search: state.search,
      filters: JSON.stringify(state.filters),
      sorting: JSON.stringify(state.sorting),
      aggregationAttributes: JSON.stringify(state.aggregationAttributes),
      limit: pageLength,
    }
    const data = await getMany(request)
    const { results, total_count, aggregations } = data
    loading.value = false
    searchQueryFinished.value = true
    initialized.value = true
    projecten.value = results
    totalCount.value = total_count
    // @ts-ignore
    projectAggregations.value = aggregations
  }

  watchDebounced(
    state,
    () => {
      if ((!getDataWithoutQuery && state.search) || getDataWithoutQuery) {
        getData()
      }

      if (!getDataWithoutQuery && !state.search) {
        projecten.value = []
      } else {
        searchQueryFinished.value = false
      }
    },
    {
      debounce: 250,
      immediate: getDataWithoutQuery,
    },
  )

  return {
    // constants
    pageLength,
    nPages,

    // results
    loading,
    searchQueryFinished,
    initialized,
    projecten,
    totalCount,
    projectAggregations,
  }
}
