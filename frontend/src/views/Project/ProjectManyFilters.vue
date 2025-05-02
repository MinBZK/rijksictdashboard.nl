<template>
  <v-list nav>
    <strong>{{ label }}</strong>
    <v-list-item
      v-for="{ aggregation_value } in values"
      :key="aggregation_value"
      class="filter-item mb-0 pb-0"
      role="menuitemcheckbox"
      :aria-label="`Filteren op ${aggregation_value}`"
      aria-checked="true"
      aria-disabled="false"
      tabindex="0"
    >
      <v-checkbox
        v-if="aggregation_value"
        v-model="filteredValues"
        :label="`${aggregation_value}`"
        :hide-details="false"
        :value="aggregation_value"
        density="compact"
        :disabled="disabled"
      />
    </v-list-item>
  </v-list>
</template>

<script setup lang="ts">
import type { AttributeAggregation } from "@/types/project"

const props = withDefaults(
  defineProps<{
    attribute: string
    values: AttributeAggregation[]
    label: string
    appliedFilterValues?: string[]
    disabled: boolean
  }>(),
  {
    appliedFilterValues: () => [],
  },
)

const filteredValues = ref<string[]>([])

const emit = defineEmits<{
  (e: "updateFilters", values: string[]): void
}>()

watch(filteredValues, (newValues) => {
  emit("updateFilters", newValues)
})

// watch number of filters
// for some reason, watching the applied filters directly doesn't work
const nFilters = computed(() => props.appliedFilterValues.length)
watch(nFilters, () => {
  filteredValues.value = props.appliedFilterValues
})
</script>

<style scoped lang="scss">
.filter-item {
  padding-top: 0 !important;
  margin-bottom: 0;
  min-height: 0 !important;
}

.filter-item:deep(.v-input__details) {
  display: none;
}

.filter-item:deep(.v-input--density-compact) {
  --v-input-control-height: 1.5em;
}
</style>
