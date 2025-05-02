<template>
  <div :id="containerId" ref="chartContainer" :aria-label="title" />
</template>

<script setup lang="ts">
// @ts-ignore
import Highcharts from "highcharts"
import exportingInit from "highcharts/modules/accessibility"
exportingInit(Highcharts)
import colorsConfig from "@/config/colors"
import type { LineChartDatapoint } from "@/types/chart"
import type { ProjectAttributePrimitiveDataType } from "@/types/project"
import type {
  ChartType,
  ChartHorizontalLine,
  ChartDataLabel,
} from "@/types/chart"
import { dateToLocaleDateString, formatValue } from "@/util"

const containerId = "linechart-container" + Math.floor(Math.random() * 10000)

type HighchartsProps = {
  chartData: LineChartDatapoint[]
  xDataType: ProjectAttributePrimitiveDataType
  yDataType: ProjectAttributePrimitiveDataType
  labelHorizontal: string
  labelHorizontalTable: string
  labelMeasure: string
  chartType?: ChartType
  type?: string
  colors?: string[]
  ordering?: string
  gap?: number
  sortedCategories?: string[]
  yAxisInteger?: boolean
  height?: number
  horizontalLine?: ChartHorizontalLine
  dataLabels?: ChartDataLabel
  title: string
  hideLegendIfOnlyOneSerie?: boolean
}

const props = withDefaults(defineProps<HighchartsProps>(), {
  chartType: "timeLine",
  type: "grouped",
  gap: 20,
  yAxisIntegers: false,
  dataLabels: () => {
    return {
      enabled: false,
    }
  },
})

const chartTypeMapping: { [key in ChartType]: string } = {
  barChart: "column",
  timeLine: "line",
  pieChart: "pie",
  HorizontalBarChart: "bar",
}

const categories = computed(
  () =>
    props.sortedCategories || [
      ...new Set(props.chartData.map((datapoint) => datapoint.x)),
    ],
)

const serieNames = computed(() => [
  ...new Set(props.chartData.map((datapoint) => datapoint.label)),
])

const sharedFormatter = (yValue: string | number, yDataType: string) => {
  if (yDataType === "currency-million") {
    return formatValue(yValue, {
      dataType: props.yDataType,
    })
  } else if (yDataType === "percentage") {
    return formatValue(yValue, {
      dataType: props.yDataType,
      maximumDigits: 0,
    })
  } else if (yDataType === "number") {
    return formatValue(yValue, { dataType: props.yDataType })
  }
  return yValue
}

const tooltipOption = computed(() => {
  if (props.chartType === "pieChart") {
    return {
      enabled: false,
    }
  } else if (props.chartType === "timeLine" || props.chartType === "barChart") {
    // @ts-ignore
    const formatter = function () {
      // @ts-ignore
      const formatterData = this as {
        x: string | number
        y: string | number
      }
      const xValue = formatterData.x
      // @ts-ignore
      const yValue = formatterData.y

      let tooltipText = ""

      if (props.chartType === "timeLine") {
        const date = dateToLocaleDateString(new Date(xValue))
        tooltipText = `<strong>${date}</strong>: `
      } else if (props.chartType === "barChart") {
        tooltipText = `<strong>${xValue}</strong>: `
      }

      tooltipText += sharedFormatter(yValue, props.yDataType)
      return tooltipText
    }

    return {
      formatter,
    }
  } else {
    return {
      tooltip: null,
    }
  }
})

const getDatapointValue = (serieName: string, category: string) => {
  const datapoint = props.chartData.find(
    (datapoint) => datapoint.label == serieName && datapoint.x == category,
  )
  return datapoint
}

const chartDataHighcharts = computed(() => {
  return serieNames.value.map((serieName) => {
    let seriesData = []

    if (props.chartType == "pieChart") {
      seriesData = categories.value
        .map((c) => {
          return {
            name: c,
            y: parseFloat(String(getDatapointValue(serieName, c)?.y)) || 0,
          }
        })
        .sort((a, b) => b.y - a.y)
    } else if (props.chartType == "timeLine") {
      const sortedCategories = [...categories.value].sort()
      seriesData = sortedCategories.map((c) => {
        const datapointValue = getDatapointValue(serieName, c)?.y
        return [new Date(Date.parse(c.toString())).getTime(), datapointValue]
      })
    } else {
      seriesData = categories.value.map((c) => {
        const datapoint = getDatapointValue(serieName, c)
        return {
          y: datapoint?.y || 0,
          sortValue: datapoint?.sortValue,
        }
      })
    }

    return {
      name: serieName,
      data: seriesData,
    }
  })
})

const titleDescription = computed(() => `Grafiek over ${props.title}`)

const highChartsChartType = computed(() => chartTypeMapping[props.chartType])

Highcharts.setOptions({
  credits: {
    enabled: false,
  },
  title: {
    text: undefined,
  },
  tooltip: {
    backgroundColor: "white",
    shadow: false,
    borderWidth: "1",
    borderColor: colorsConfig.grijs3,
  },
  chart: {
    styledMode: false,
    style: {
      fontFamily: "RO Sans",
      fontSize: "1.2rem",
    },
    borderColor: "black",
    height: props.height,
  },
  colors: props.colors,
  plotOptions: {
    series: {
      animation: false,
    },
  },
  lang: {
    // docs: https://api.highcharts.com/highcharts/lang.accessibility
    accessibility: {
      svgContainerLabel: "Interactieve grafiek",
      chartContainerLabel: props.title,
      defaultChartTitle: titleDescription.value,
      legend: {
        legendLabelNoTitle: `Verberg of toon grafiek, ${props.title}.`,
        legendItem: "Toon {itemName}.",
      },
      axis: {
        xAxisDescriptionSingular:
          "De grafiek heeft 1 horizontale as en toont {names[0]}. {ranges[0]}",
        yAxisDescriptionSingular:
          "De grafiek heeft 1 verticale as en toont {names[0]}. {ranges[0]}",
        rangeCategories: "Data bereik: {numCategories} categorieën.",
        rangeFromTo: "Data bereik van {rangeFrom} tot {rangeTo}.",
        timeRangeDays: "Data bereik: {range} dagen.",
        timeRangeHours: "Data bereik: {range} uren.",
        timeRangeMinutes: "Data bereik: {range} minuten.",
        timeRangeSeconds: "Data bereik: {range} seconden.",
      },
      chartTypes: {
        barMultiple: "Staafgrafiek met {numSeries} data series.",
        barSingle:
          "Staafgrafiek with {numPoints} {#eq numPoints 1}staaf{else}staven{/eq}.",
        columnMultiple: "Staafgrafiek met {numSeries} data series.",
        columnSingle:
          "Staafgrafiek met {numPoints} {#eq numPoints 1}staaf{else}staven{/eq}.",
        lineSingle:
          "Lijngrafiek met {numPoints} data{#eq numPoints 1}punt{else}punten{/eq}.",
        lineMultiple: "Lijngrafiek met {numSeries} lijnen.",
        pieSingle:
          "Taartgrafiek met {numPoints} {#eq numPoints 1}slice{else}slices{/eq}.",
        pieMultiple: "Taartgrafiek met {numSeries} taarten.",
      },
      series: {
        summary: {
          // For some reason, the if else logic in the Highcharts templating does not work.
          // Example: {#eq series.points.length 1}staaf{else}staven{/eq} becomes 'staafstaven'
          // Source: https://api.highcharts.com/highcharts/lang.accessibility.series.summary.column
          // bar: "{series.name}, staafgrafiek serie {seriesNumber} van {chart.series.length} met {series.points.length} {#eq series.points.length 1}staaf{else}staven{/eq}.",
          // column:
          //   "{series.name}, staafgrafiek serie {seriesNumber} van {chart.series.length} met {series.points.length} {#eq series.points.length 1}staaf{else}staven{/eq}.",
          bar: "{series.name}, staafgrafiek serie {seriesNumber} van {chart.series.length} met {series.points.length} staven.",
          column:
            "{series.name}, staafgrafiek serie {seriesNumber} van {chart.series.length} met {series.points.length} staven.",
          line: "{series.name}, lijn {seriesNumber} van {chart.series.length} met {series.points.length} data{#eq series.points.length 1}punt{else}punten{/eq}.",
          pie: "{series.name}, taart {seriesNumber} van {chart.series.length} met {series.points.length} {#eq series.points.length 1}punt{else}punten{/eq}.",
        },
      },
    },
    months: [
      "januari",
      "februari",
      "maart",
      "april",
      "mei",
      "juni",
      "juli",
      "augustus",
      "september",
      "oktober",
      "november",
      "december",
    ],
    shortMonths: [
      "jan",
      "feb",
      "mar",
      "apr",
      "mei",
      "jun",
      "jul",
      "aug",
      "sep",
      "okt",
      "nov",
      "dec",
    ],
    weekdays: [
      "zondag",
      "maandag",
      "dinsdag",
      "woensdag",
      "donderdag",
      "vrijdag",
      "zaterdag",
    ],
  },
})

const plotLines = computed(() => {
  return props.horizontalLine
    ? [
        {
          color: "#000",
          width: 2,
          value: props.horizontalLine.value,
          label: {
            text: props.horizontalLine.label,
            align: "right",
            style: {
              fontSize: 12,
            },
          },
        },
      ]
    : []
})

const showLegend = computed(() =>
  props.hideLegendIfOnlyOneSerie && serieNames.value.length == 1 ? false : true,
)

const chartOptions = computed(() => {
  return {
    chart: {
      type: highChartsChartType.value,
    },
    xAxis: {
      categories: props.chartType == "timeLine" ? null : categories.value,
      title: {
        text: props.labelHorizontal,
      },
      type: props.chartType == "timeLine" ? "datetime" : "linear",
      // labels: {
      //   format: "{value:%Y-%B-%d}",
      // },
    },
    yAxis: {
      plotLines: plotLines.value,
      title: {
        text: props.labelMeasure,
      },
      labels: {
        formatter: function (): string | number {
          //@ts-ignore
          const v = this.value
          return formatValue(v, {
            dataType: props.yDataType,
            maximumDigits: 0,
          })
        },
      },
      minTickInterval: props.yAxisInteger ? 1 : null,
    },
    series: chartDataHighcharts.value,
    legend: {
      enabled: showLegend.value,
      verticalAlign: "bottom",
      symbolRadius: 0,
    },

    tooltip: tooltipOption.value,
    plotOptions: {
      series: {
        animation: false,
        borderColor: "black",
        borderWidth: 0.5,
        borderRadius: 0,
        dataLabels: dataLabels.value,
      },
    },
  }
})

const dataLabelFormat = computed(() => {
  if (props.dataLabels.value == "y" && props.yDataType == "percentage") {
    return "{y}%"
  } else if (props.chartType == "pieChart") {
    return `{point.name} ({y})`
  } else {
    return `{${props.dataLabels.value}}`
  }
})

const dataLabels = computed(() => {
  return {
    enabled: props.dataLabels?.enabled,
    format: props.chartType == "pieChart" ? undefined : dataLabelFormat.value,

    // the formatter is only applied when format is defined, according to Highcharts documentation
    // this formatter thus only works for a pie chart
    formatter: function (): string {
      //@ts-expect-error: this is untyped
      const { key, y } = this
      const categoryValue = key
      const yValue = y
      return `${categoryValue} (${sharedFormatter(yValue, props.yDataType)})`
    },
    style: {
      fontWeight: "normal",
    },
  }
})

function renderChart() {
  //@ts-ignore
  new Highcharts.Chart(containerId, chartOptions.value)
}

onMounted(() => renderChart())

watch(chartDataHighcharts, () => renderChart())

// This updates the aria-label on the container div and heading in a screenreader only div.
// By default, Highcharts does this based on the lang.accessibility.chartContainerLabel property.
// However, there seems to be a bug in Highcharts: when there are multiple charts on one page,
// all charts get the aria-label of the last rendered chart. Therefore, the code below overrides
// the aria label to make sure it is correct.
const chartContainer = ref<HTMLDivElement | null>(null)
watch(chartContainer, () => {
  if (chartContainer.value?.ariaLabel) {
    chartContainer.value.ariaLabel = props.title
    const children = chartContainer.value.childNodes
    children.forEach((node) => {
      const div = node as HTMLDivElement
      if (div.id.includes("screen-reader-region-before")) {
        const headings = ["h2", "h3", "h4"]
        headings.forEach((h) => {
          const headingNode = div.querySelector(h) as HTMLHeadingElement
          if (headingNode) headingNode.innerText = titleDescription.value
        })
      }
    })
  }
})
</script>
