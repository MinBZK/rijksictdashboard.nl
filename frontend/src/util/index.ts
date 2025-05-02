import type { ProjectAttributePrimitiveDataType } from "@/types/project"

const convertToSlug = (string: string) =>
  string
    .toLowerCase()
    .replace(/ /g, "-")
    .replace(/[^\w-]+/g, "")

const sortArrayByKey = <T>(
  array: T[],
  key: keyof T,
  order?: "asc" | "desc",
): T[] => {
  return [
    ...array.sort((a, b) => {
      const x = a[key] || ""
      const y = b[key] || ""
      const result = x < y ? -1 : x > y ? 1 : 0
      if (order) {
        return order === "asc" ? result : -result
      }
      return result
    }),
  ]
}

const deepClone = (object: any) => JSON.parse(JSON.stringify(object))

const getApiBaseUrl = () => import.meta.env.VITE_API_ENDPOINT
  import.meta.env.MODE == "production"
    ? `https://${window.location.host}/api`
    : import.meta.env.VITE_API_ENDPOINT

const flattenArray = <T>(arr: T[][]): T[] => {
  return arr.reduce((flatArray, arrayItem) => {
    return [...flatArray, ...arrayItem]
  }, [])
}

const getUniqueValues = <T>(arr: T[]): T[] => {
  return [...new Set(arr)]
}

const getMonthsDifferenceBetweenDates = (d1: Date, d2: Date) => {
  let months
  months = (d2.getFullYear() - d1.getFullYear()) * 12
  months -= d1.getMonth()
  months += d2.getMonth()
  return months <= 0 ? 0 : months
}

export type FormatConfig = {
  dataType: ProjectAttributePrimitiveDataType | undefined
  unitSuffix?: string | null
  maximumDigits?: number
  minimumDigits?: number
}

const formatValue = (
  value: string | number | null,
  formatConfig: FormatConfig,
) => {
  const {
    dataType,
    unitSuffix = null,
    maximumDigits = undefined,
    minimumDigits = 0,
  } = formatConfig
  const isNullOrUndefined = value === null || value === undefined
  const isNumber = typeof value == "number"
  const isString = typeof value == "string"
  let result
  if (isNullOrUndefined) {
    result = ""
  } else if (dataType == "currency" || dataType == "currency-million") {
    let maxDigits = undefined
    if (dataType == "currency-million") maxDigits = 2
    if (maximumDigits !== undefined) maxDigits = maximumDigits
    result = new Intl.NumberFormat("nl-NL", {
      style: "currency",
      currency: "EUR",
      maximumFractionDigits: maxDigits,
    }).format(isNumber ? value : parseFloat(value))

    if (dataType == "currency-million") result = result + " mln."
  } else if (dataType == "date" && isString) {
    // Dit zorgt voor 2 digits per dag en maand eenheid dus 01-01-YYYY ipv 1-1-YYYY
    result = value.substring(0, 10).split("-").reverse().join("-")
  } else if (dataType == "number") {
    const float = isString ? parseFloat(value) : value
    const floatString = float.toLocaleString("nl", {
      maximumFractionDigits: maximumDigits,
      minimumFractionDigits: minimumDigits,
    })
    result = isNaN(float) ? "Onbekend" : floatString
  } else if (dataType == "integer") {
    const integer = isString ? parseInt(value) : value
    result = isNaN(integer) ? "Onbekend" : integer
  } else if (dataType == "percentage") {
    result = value + "%"
  } else {
    result = value
  }
  return unitSuffix && value ? `${result} ${unitSuffix}` : result
}

const isValidUrl = (url: string) => {
  const regex =
    // eslint-disable-next-line
    /((([A-Za-z]{3,9}:(?:\/\/)?)(?:[-;:&=\+\$,\w]+@)?[A-Za-z0-9.-]+|(?:www.|[-;:&=\+\$,\w]+@)[A-Za-z0-9.-]+)((?:\/[\+~%\/.\w-_]*)?\??(?:[-\+=&;%@.\w_]*)#?(?:[\w]*))?)/
  return regex.test(url)
}

const dateToLocaleDateString = (date: Date) =>
  date.toLocaleDateString("nl", {
    year: "numeric",
    month: "long",
    day: "numeric",
  })

const capitalizeFirstLetter = (string: string) =>
  string.charAt(0).toUpperCase() + string.slice(1)

const arrayIsDeepEqual = (arr1: any[], arr2: any[]) =>
  JSON.stringify(arr1) == JSON.stringify(arr2)

function getObjectKeys<T extends Record<string, any>>(obj: T): (keyof T)[] {
  return Object.keys(obj) as (keyof T)[]
}

export {
  convertToSlug,
  sortArrayByKey,
  deepClone,
  getApiBaseUrl,
  flattenArray,
  getUniqueValues,
  getMonthsDifferenceBetweenDates,
  formatValue,
  isValidUrl,
  dateToLocaleDateString,
  capitalizeFirstLetter,
  arrayIsDeepEqual,
  getObjectKeys,
}
