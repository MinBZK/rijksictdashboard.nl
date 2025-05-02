import { KwivDataService, KwivJaar } from "@/api-new"

type KwivRequest = {
  jaar: KwivJaar
  ministerie?: string | null
  category?: string | null
}

const getKwivData = (request: KwivRequest) =>
  KwivDataService.kwivKwivGet(request)

export { getKwivData }
