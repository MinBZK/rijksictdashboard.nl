<template>
  <div v-if="metricValue !== undefined">
    <v-card-item
      class="text pb-2 metric-title"
      :class="fixedTitleHeight && 'fixed-title-height'"
      >{{ title }}

      <InformationIcon v-if="caption" :caption="caption" :label="title" />
    </v-card-item>
    <v-card-text class="text-h4 text-primary">
      <template v-if="!filters">
        {{ formattedValue }}
      </template>
      <template v-else>
        <router-link
          :to="{
            name: 'ICT-activiteiten',
            query: {
              filters: stringifyArray(filters, 'filters'),
              sorting: stringifyArray(sorting || [], 'sorting'),
            },
          }"
        >
          {{ formattedValue || 0 }}
        </router-link>
      </template>
    </v-card-text>
  </div>
</template>

<script setup lang="ts">
import type {
  AttributeSorting,
  ProjectAttributePrimitiveDataType,
} from "@/types/project"
import { formatValue } from "@/util"
import InformationIcon from "./InformationIcon.vue"
import { stringifyArray } from "@/util/querystring"
import type { ProjectFilter } from "@/types/project"

const props = withDefaults(
  defineProps<{
    title: string
    metricValue?: number
    dataType?: ProjectAttributePrimitiveDataType
    unitSuffix?: string
    maxDigits?: number
    caption?: string
    filters?: ProjectFilter[]
    sorting?: AttributeSorting[]
    fixedTitleHeight?: boolean
  }>(),
  {
    fixedTitleHeight: false,
  },
)

const formattedValue = computed(() => {
  return props.metricValue
    ? formatValue(props.metricValue, {
        dataType: props.dataType,
        unitSuffix: props.unitSuffix,
        maximumDigits: props.maxDigits,
      })
    : null
})
</script>

<style lang="scss" scoped>
.metric-title {
  display: block;
}

.fixed-title-height {
  height: 4em;
}

// .metric-title:deep(.v-card-item__content) {
//   bottom: 0;
//   position: absolute;
// }

:deep(.v-card-text) {
  line-height: 0.9em;
}
</style>
