import type {
  Ministeries,
  Onderwerpen,
  RapportageGeschiedenis,
} from "@/types/content"
import ministerie from "@/content/ministerie"
import onderwerp from "@/content/onderwerp"
import rapportageGeschiedenis from "@/content/rapportageschiedenis"

type ContentStore = {
  ministerie: Ministeries
  onderwerp: Onderwerpen
  rapportageGeschiedenis: RapportageGeschiedenis[]
}

const content = reactive({
  ministerie,
  onderwerp,
  rapportageGeschiedenis,
} as ContentStore)

export function useContent() {
  return { content }
}
