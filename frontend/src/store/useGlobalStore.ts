import { useRouteQuery } from "@vueuse/router"
import type { Project } from "@/api-new"

type State = {
  currentProject: Project | null
  loadingCurrentProject: boolean
  activiteiten: Project[]
  ministeries: string[]
}

const state = reactive({
  currentProject: null,
  loadingCurrentProject: false,
} as State)

export function useGlobalStore() {
  const contentOnly = computed(() => {
    const contentOnly = useRouteQuery("contentOnly").value || ""
    return Array.isArray(contentOnly) ? false : parseInt(contentOnly) == 1
  })

  return { contentOnly, state }
}
