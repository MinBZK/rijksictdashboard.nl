import { getMany } from "@/services/project"
import type { ProjectenMetMetrics } from "@/api-new"
import type { ProjectStatus } from "@/types/project"
import type { Ref } from "vue"
import type { ProjectFilter } from "@/types/project"

type StatusType = "all" | "allActive"

type MetricsStoreData = {
  data?: ProjectenMetMetrics
  loading: boolean
}

// type MetricsStoreDatasets = {
//   all?: MetricsStoreData
//   allActive?: MetricsStoreData
// }

type MetricsStore = {
  [key: string]: MetricsStoreData
}

const state = reactive({} as MetricsStore)

interface MetricsInput {
  statusType: StatusType
  autoLoad?: boolean
  filters?: Ref<ProjectFilter[]>
}

export function useMetrics(input: MetricsInput) {
  const {
    statusType,
    autoLoad = true,
    filters = ref<ProjectFilter[]>([]),
  } = input

  const status = (
    statusType == "allActive"
      ? ["In heroriëntatie", "In uitvoering"]
      : ["In heroriëntatie", "In uitvoering", "Afgerond", "Geannuleerd"]
  ) as ProjectStatus[]

  const allFilters = computed(() => {
    return [...filters.value, { attribute: "ProjectStatus", values: status }]
  })

  const stringifiedFilters = computed(() => JSON.stringify(allFilters.value))
  const storeKey = computed(() => stringifiedFilters.value + statusType)

  const getData = async () => {
    const inState = !!state[storeKey.value]
    if (!inState) {
      state[storeKey.value] = { loading: true }
    }

    const hasData = state[storeKey.value].loading === false

    if (!hasData) {
      const data = await getMany({
        filters: stringifiedFilters.value,
        getProjects: true,
      })

      state[storeKey.value] = {
        loading: false,
        data,
      }
    }
  }

  const projectenMetMetrics = ref<ProjectenMetMetrics | null>(null)
  const selectedMetrics = computed(() => state[storeKey.value]?.data)
  const loading = computed(() => {
    return state[storeKey.value]?.loading == true
  })

  watch(
    selectedMetrics,
    () => {
      // only update metrics after the data has been loaded
      if (selectedMetrics.value) {
        projectenMetMetrics.value = selectedMetrics.value
      }
    },
    { immediate: true },
  )

  watch(
    filters,
    () => {
      if (autoLoad) getData()
    },
    {
      immediate: true,
    },
  )

  const metrics = computed(() => projectenMetMetrics.value?.metrics)

  return { projectenMetMetrics, metrics, loading, getData }
}
