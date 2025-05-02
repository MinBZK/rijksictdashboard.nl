import { IctKostenService } from "@/api-new"

const getIctKosten = (ministerie: string | null) =>
  IctKostenService.kostenstelselsIctKostenGet({ ministerie })

export { getIctKosten }
