import { getApiBaseUrl } from "@/util"
import { AggregatieService, ApiError, ProjectService } from "@/api-new"

// type Query = {
//   page?: number
//   limit?: number | null
//   search?: string
//   filters?: ProjectFilter[]
//   sorting?: AttributeSorting[]
//   get_aggregations?: boolean
// }

// type ExcludeFilter = Omit<Query, "filters" | "sorting">

// interface RequestQuery extends ExcludeFilter {
//   filters?: string
//   sorting?: string
// }

type ProjectGetMany = {
  limit?: number | null
  page?: number
  search?: string | null
  getProjects?: boolean
  filters?: string | null
  sorting?: string | null
  aggregationAttributes?: string | null
}

const getMany = async (request: ProjectGetMany = {}) => {
  return ProjectService.getManyProjectGet(request)
}

const getOne = (
  id: string,
  projectVersieId: number | undefined,
  token: string | undefined,
  isLegacyProjectId: boolean,
) =>
  ProjectService.getOneProjectUnparsedProjectIdGet({
    unparsedProjectId: id,
    projectVersieId,
    token,
    isLegacyId: isLegacyProjectId,
  })
    .then(async (response) => {
      const projecten = response
      return { data: projecten, error: null }
    })
    .catch((e) => {
      const error = e as ApiError
      return {
        data: null,
        error:
          error.status == 401
            ? "De previewlink is verlopen, maak een nieuwe aan in de beheermodule."
            : error.body.detail,
      }
    })

// projectApi
//   .getOneProjectProjectIdGet({
//     projectId: id,
//     projectVersieId,
//     token,
//   })
//   .then(async (response) => {
//     const projecten = response.data
//     return { data: projecten, error: null }
//   })
//   .catch((e) => {
//     const error = e as AxiosError
//     if (error.response?.data) {
//       const errorDetail = error.response.data as ApiHttpError
//       return { data: null, error: errorDetail.detail }
//     } else {
//       return { data: null, error: "Server error" }
//     }
//   })

// const getAggregation = (
//   request: AggregatieApiAggPerAttributeProjectAggregatieAggAttributeGetRequest
// ) =>
//   aggregatieApi
//     .aggPerAttributeProjectAggregatieAggAttributeGet(request)
//     .then((response) => response.data)

type AggRequest = {
  attribute: string
  filters?: string | null
}

const getAggregation = (request: AggRequest) =>
  AggregatieService.aggPerAttributeProjectAggregatieAggAttributeGet(request)

const projectSpreadsheetUrl = (
  spreadsheetType: SpreadsheetType,
  project_id: string,
) => `${getApiBaseUrl()}/opendata/spreadsheet/${spreadsheetType}/${project_id}`

const jsonUrl = `${getApiBaseUrl()}/opendata/json`

export type SpreadsheetType = "excel" | "ods"

const spreadsheetUrl = (spreadsheetType: SpreadsheetType) =>
  `${getApiBaseUrl()}/opendata/spreadsheet/${spreadsheetType}`

export {
  getMany,
  getOne,
  getAggregation,
  projectSpreadsheetUrl,
  jsonUrl,
  spreadsheetUrl,
}
