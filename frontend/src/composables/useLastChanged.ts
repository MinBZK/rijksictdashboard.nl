import type { Ref } from "vue"
import type { ProjectProps } from "@/composables/useProjecten"
import type { ProjectMetCoreMetrics } from "@/api-new"
import type { ProjectFilter } from "@/types/project"
import { getMany } from "@/services/project"

type FetchState = {
  loading: boolean
  data: ProjectMetCoreMetrics[]
}

const store: Record<string, FetchState> = reactive({})

export const useLastChanged = (ministerie: Ref<string | undefined>) => {
  const filters = computed((): ProjectFilter[] => {
    if (ministerie.value) {
      return [
        {
          attribute: "MinisterieNaam",
          values: [ministerie.value],
        },
      ]
    } else {
      return []
    }
  })

  const state: ProjectProps = reactive({
    filters,
    sorting: [
      {
        attribute: "ProjectVersieWijzigingsDatum",
        direction: "desc",
      },
    ],
    limit: 10,
  })

  const ministerieKey = computed(() => ministerie.value || "none")

  const loading = computed(() => store[ministerieKey.value]?.loading || false)

  const projecten = computed(
    () => store[ministerieKey.value]?.data || ([] as ProjectFilter[]),
  )

  async function getData() {
    if (!loading.value) {
      if (store[ministerieKey.value]) {
        store[ministerieKey.value].loading = true
      } else {
        store[ministerieKey.value] = { loading: true, data: [] }
      }

      const { results } = await getMany({
        limit: 10,
        filters: JSON.stringify(state.filters),
        sorting: JSON.stringify(state.sorting),
      })
      store[ministerieKey.value].data = results
    }
  }

  watch(
    ministerie,
    () => {
      getData()
    },
    {
      immediate: true,
    },
  )

  return {
    projecten,
  }
}
