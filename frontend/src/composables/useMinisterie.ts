import ministerieService from "@/services/ministerie"
import type { Ministerie } from "@/api-new"

const ministeries = ref<Ministerie[]>([])

const getMinisteries = async () => {
  ministeries.value = await ministerieService.getAll()
}

export const useMinisterie = () => {
  if (ministeries.value.length == 0) getMinisteries()

  return {
    ministeries,
  }
}
