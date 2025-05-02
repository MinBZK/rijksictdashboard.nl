import { getApiBaseUrl } from "@/util"

const downloadJBRFile = (year: number) =>
  `${getApiBaseUrl()}/jbr-file/activiteiten/${year}`

export { downloadJBRFile }
