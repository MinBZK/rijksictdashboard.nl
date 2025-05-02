import type { LineChartDatapoint } from "@/types/chart"

export type IctKostenDataPoint = {
  kostenpost: string
  categorie: string
  ministerie: string
  kosten: number
}

export type IctKosten = {
  graph_data_kv: LineChartDatapoint[]
  graph_data_bl: LineChartDatapoint[]
  kosten_kasverplichtingenstelsel: IctKostenDataPoint[]
  kosten_batenlastenstelsel: IctKostenDataPoint[]
  available_ministeries: string[]
}
