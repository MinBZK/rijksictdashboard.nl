export type LineChartDatapoint = {
  x: string
  y: string | number | null
  label: string
  sortValue?: string | number
}

export type ChartCaptionPosition = "right" | "top" | "hidden"

export type ChartType =
  | "barChart"
  | "timeLine"
  | "pieChart"
  | "HorizontalBarChart"

export type ChartHorizontalLine = {
  value: number
  label: string
}

export type ChartDataLabel = {
  enabled: boolean
  value?: "x" | "y" | "point.name"
}
