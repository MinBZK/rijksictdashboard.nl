import { ZoekenService } from "@/api-new"

const search = (q: string, c?: string) =>
  ZoekenService.searchSearchSearchQueryGet({
    searchQuery: q,
    category: c || undefined,
  })

export { search }
