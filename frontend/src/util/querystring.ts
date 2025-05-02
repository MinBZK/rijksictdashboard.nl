import * as qs from "qs"

const stringifyArray = (array: any[], key: "filters" | "sorting") => {
  return qs.stringify({ [key.charAt(0)]: array })
}

const parseRouteQueryString = (
  queryString: string | undefined,
  routeQueryKey: string,
) => {
  if (queryString) {
    const parsed = qs.parse(queryString)
    return parsed?.[routeQueryKey] || []
  } else {
    return []
  }
}

export { stringifyArray, parseRouteQueryString }
