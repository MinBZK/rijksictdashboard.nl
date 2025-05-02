<template>
  <Page
    :title="attributeValue"
    :title-category="attributeLabel"
    :description="description"
  >
    <slot />

    <Metrics :filters="filters" :introduction-text-with-link="true" />
    <ProjectManyTiles :projecten="projecten" />
    <TileSlider
      v-if="secondAttribute"
      :slider-data="getSliderData(secondAttribute, true)"
      :title="props.secondAttributeSliderTitle"
    />
    <TileSlider
      :slider-data="getSliderData(attribute)"
      :title="`Andere ${pluralLabel}`"
    />
  </Page>
</template>

<script setup lang="ts">
import Page from "@/components/Page.vue"
import ProjectManyTiles from "@/views/Project/ProjectManyTiles.vue"
import type { ProjectAttribute } from "@/types/project"
import Metrics from "@/views/Common/Metrics.vue"
import type { ProjectFilter } from "@/types/project"
import TileSlider from "@/components/TileSlider.vue"
import cmsConfig from "@/config/cms"
import { useProjecten } from "@/composables/useProjecten"
import { sortArrayByKey } from "@/util"
import { stringifyArray } from "@/util/querystring"

const props = defineProps<{
  attribute: ProjectAttribute
  attributeLabel: string
  attributeValue: string
  secondAttribute?: ProjectAttribute
  showOtherAttributeValues?: boolean
  secondAttributeSliderTitle?: string
  description?: string
}>()

const filters = computed(() => {
  const filters: ProjectFilter[] = [
    { attribute: props.attribute, values: [props.attributeValue] },
  ]
  return filters
})

const state = computed(() =>
  reactive({
    filters: filters,
    limit: 100,
    aggregationAttributes: props.secondAttribute
      ? [props.secondAttribute, props.attribute]
      : [props.attribute],
  }),
)

const { projectAggregations, projecten } = useProjecten({
  state: state.value,
})

const pluralLabel = computed(() => {
  if (Object.keys(cmsConfig.attributeConfig).includes(props.attribute)) {
    return `${cmsConfig.attributeConfig[props.attribute]?.pluralLabel}`
  } else {
    console.error(`No labels defined for attribute ${props.attribute}`)
  }
})

function getSliderData(
  attribute: ProjectAttribute,
  sortOnCount: boolean = false,
) {
  const data =
    projectAggregations.value.find(
      (pA) => pA.aggregation_attribute == attribute,
    )?.values || []

  const sortedData =
    attribute == props.secondAttribute
      ? sortArrayByKey(data, "count").reverse()
      : sortArrayByKey(data, "aggregation_value")

  const sliderData = sortedData
    .filter((v) => {
      const notNullValue = v.aggregation_value && v.aggregation_value.length > 0
      // exclude values that are the primary attribute.
      // For example: if attribute prop is 'Onderwerp' and attributeValue prop 'Economie', then exclude 'Economie' from the slider.
      const isPrimaryAttributeValue =
        v.aggregation_column == props.attribute &&
        v.aggregation_value == props.attributeValue
      return notNullValue && !isPrimaryAttributeValue
    })
    .map((aV) => {
      return {
        title: aV.aggregation_value,
        subtitle: `${aV.count} ICT-activiteiten`,
        route: {
          name: cmsConfig.attributeConfig[attribute]?.routerName,
          params: { attributeValue: aV.aggregation_value },
        },
        subtitleRoute: {
          name: "ICT-activiteiten",
          query: {
            filters: stringifyArray(
              attribute == props.secondAttribute
                ? [
                    {
                      attribute: props.secondAttribute,
                      values: [aV.aggregation_value],
                    },
                    {
                      attribute: props.attribute,
                      values: [props.attributeValue],
                    },
                  ]
                : [
                    {
                      attribute: props.attribute,
                      values: [aV.aggregation_value],
                    },
                  ],
              "filters",
            ),
          },
        },
        sortValue: sortOnCount ? aV.count : undefined,
      }
    })

  return sliderData
}
</script>
