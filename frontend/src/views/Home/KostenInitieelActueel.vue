<template>
  <div class="text-h4 text-primary text-center mt-6">
    <strong>{{ Number(delta || 0).toFixed(0) }}%</strong>
  </div>

  <p class="text-center mb-8">Verschil in procenten</p>
  <RidCardMetricContent
    v-for="(v, index) in getObjectKeys(values)"
    :key="v"
    :data-type="dataType"
    :unit-suffix="unitSuffix"
    :max-digits="maxDigits"
    :title="v"
    :metric-value="kengetallen?.[values[v]]"
    :class="index < Object.keys(values).length - 1 && 'mb-3'"
  ></RidCardMetricContent>
</template>

<script setup lang="ts">
import { useMetrics } from "@/composables/useMetrics"
import type { ProjectAttributePrimitiveDataType } from "@/types/project"
import RidCardMetricContent from "@/components/RidCardMetricContent.vue"
import type { ProjectFilter } from "@/types/project"
import { getObjectKeys } from "@/util"

const props = withDefaults(
  defineProps<{
    ministerie?: string
    autoLoad?: boolean
  }>(),
  {
    autoLoad: true,
  },
)

const filters = computed(() => {
  const filters: ProjectFilter[] = props.ministerie
    ? [{ attribute: "MinisterieNaam", values: [props.ministerie] }]
    : []
  return filters
})

const { metrics } = useMetrics({
  filters,
  statusType: "allActive",
  autoLoad: props.autoLoad,
})

const values = {
  "Eerste schatting": "SchattingTotaleKostenInitieel (sum)",
  "Schatting nu": "SchattingTotaleKostenHuidigJaar (sum)",
}

const dataType = "currency" as ProjectAttributePrimitiveDataType
const unitSuffix = "mln."
const maxDigits = 0

const kengetallen = computed(() => metrics.value?.kengetallen)

const delta = computed(
  () => kengetallen.value?.["Geschatte kosten verschil in %"],
)
</script>
