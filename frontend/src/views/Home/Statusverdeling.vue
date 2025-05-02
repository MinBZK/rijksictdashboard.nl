<template>
  <RidCardMetricContent
    v-for="(value, key) in statusVerdelingActueel"
    :key="key"
    :title="key.toString()"
    data-type="number"
    :max-digits="10"
    :metric-value="value"
    :filters="[{ attribute: 'ProjectStatus', values: [key.toString()] }]"
  />
</template>

<script setup lang="ts">
import { useMetrics } from "@/composables/useMetrics"
import RidCardMetricContent from "@/components/RidCardMetricContent.vue"
import type { ProjectFilter } from "@/types/project"

const props = defineProps<{
  ministerie?: string
}>()

const filters = computed(() => {
  const filters: ProjectFilter[] = props.ministerie
    ? [{ attribute: "MinisterieNaam", values: [props.ministerie] }]
    : []
  return filters
})

const { metrics } = useMetrics({
  filters,
  statusType: "all",
  autoLoad: false,
})

const statusVerdelingActueel = computed(
  () => metrics.value?.kengetallen?.["Aantal ICT projecten per status"],
)
</script>
