import type { LineChartDatapoint } from "@/types/chart"

export type ActiviteitWithMetrics = { [key: string]: any }

// export type Metrics = {
//   kengetallen: MetricsNumbers | null
//   activiteiten: ActiviteitWithMetrics[]
//   ministeries: string[]
// }

export type MetricsNumbers = {
  "Aantal grote ICT-activiteiten": number
  "Aantal gestarte activiteiten": LineChartDatapoint[]
  "Aantal ICT projecten per status": { [key: string]: number }
  "DoorlooptijdActueel (mean)": number
  "Aantal BIT-adviezen": number
  "SchattingTotaleKostenHuidigJaar (sum)": number
  "SchattingTotaleKostenInitieel (sum)": number
  "Geschatte kosten verschil in %": number
  "Geschatte kosten per categorie": { [key: string]: number }
  "Doorlooptijd (aantallen)": { [key: string]: number }
  "Herijkingen aantal per redenen": { [key: string]: number }
  "Meest recente jaar met kosten": number
  "AantalBehaaldeMijlpalen (sum)": number
}

export type MetricsNumbersKey = keyof MetricsNumbers
