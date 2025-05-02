import type {
  ChartType,
  ChartCaptionPosition,
  ChartDataLabel,
} from "@/types/chart"
import type { MetricsNumbers } from "@/types/metrics"
import { useTextLoader } from "@/composables/useTextLoader"
const { getContent } = useTextLoader()

type MetricChartDefinition = {
  labelHorizontal: string
  labelMeasure: string
  colors?: string[]
  chartType: ChartType
  title: string
  caption?: string
  captionPosition?: ChartCaptionPosition
  xAxisSorting?: string[]
  yAxisInteger?: boolean
  dataLabels?: ChartDataLabel
}

type MetricKeys = keyof MetricsNumbers

const getMetricChartConfig = () => {
  const metricChartsConfig: { [K in MetricKeys]?: MetricChartDefinition } = {
    "Geschatte kosten per categorie": {
      labelHorizontal: "Kostengroep in miljoenen euro's",
      labelMeasure: "Aantal grote ICT-activiteiten",
      chartType: "barChart",
      title: getContent("Grafieken", "GrafiekKostenCategorie").value,
      caption: getContent("Grafieken", "KostenCategorieTitel").value,
      captionPosition: "hidden",
      yAxisInteger: true,
    },
    "Doorlooptijd (aantallen)": {
      labelHorizontal:
        "Verschil in duur bij eerste schatting en schatting duur nu",
      labelMeasure: "Aantal ICT-activiteiten",
      chartType: "barChart",
      title: getContent("Grafieken", "DoorlooptijdAantallenTitel").value,
      // caption: [
      //   "De doorlooptijden van een activiteit kunnen om diverse redenen worden aangepast. Deze grafiek toont aan hoeveel activiteiten een wijziging hebben gehad in de doorlooptijd ten opzichte van de initiële planning.",
      // ],
      caption: getContent("Grafieken", "GrafiekDoorlooptijdAantallen").value,
      xAxisSorting: ["Eerder", "Ongewijzigd", "Later ≤1 jaar", "Later >1 jaar"],
      yAxisInteger: true,
    },
    "Herijkingen aantal per redenen": {
      labelHorizontal: "Doorlooptijdwijziging",
      labelMeasure: "Aantal",
      chartType: "pieChart",
      title: getContent("Grafieken", "DoorlooptijdwijzigingRedenenTitel").value,
      // caption: [
      //   "De doorlooptijden van een activiteit kunnen om diverse redenen worden aangepast. De grafiek ‘Aangepaste doorlooptijd’ is een weergave van het aantal projecten waarvan de doorlooptijd afwijkt van de verwachte doorlooptijd.",
      //   "De meest voorkomende redenen voor aanpassingen van een activiteit zijn weergegeven in de grafiek ‘Redenen voor wijzigingen’. Deze significante wijzigingen (“herijking”) worden altijd aan de Tweede Kamer gemeld.",
      // ],
      caption: getContent("Grafieken", "GrafiekDoorlooptijdwijzigingRedenen")
        .value,
      captionPosition: "right",
      dataLabels: {
        enabled: true,
        value: "point.name",
      },
    },
  }
  return metricChartsConfig
}
export { getMetricChartConfig }
