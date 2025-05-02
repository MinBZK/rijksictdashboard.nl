<template>
  <DropdownSelectMultiple
    v-model="selectedValues"
    :items="items"
    item-label-key="title"
    item-value-key="value"
    :label="label"
  />
</template>

<script setup lang="ts">
import type { AttributeAggregation, ProjectAttribute } from "@/types/project"
import type { ProjectFilter } from "@/types/project"
import { sortArrayByKey } from "@/util"
import { arrayIsDeepEqual } from "@/util"
import DropdownSelectMultiple from "@/components/DropdownSelectMultiple.vue"
import type { ItemSelect } from "@/types/components"

const props = defineProps<{
  attribute: ProjectAttribute
  values: AttributeAggregation[]
  columnName: string
  filters?: ProjectFilter
}>()

const selectedValues = ref<ItemSelect[]>([])

const items = computed(() => {
  return sortArrayByKey(props.values, "aggregation_value").map(
    (v): ItemSelect => {
      return {
        value: v.aggregation_value,
        title: (v.aggregation_value || "(niet ingevuld)") + ` (${v.count}) `,
      }
    },
  )
})

const label = ref<string>(props.columnName)

const filters = toRef(props, "filters")
watch(
  filters,
  () => {
    selectedValues.value = filters.value
      ? items.value.filter((item) => filters.value?.values.includes(item.value))
      : []
  },
  {
    immediate: true,
    deep: true,
  },
)

const emit = defineEmits<{
  (e: "update", value: string[]): void
}>()

watch(selectedValues, (oldValue, newValue) => {
  const isUpdated = !arrayIsDeepEqual(oldValue, newValue)
  if (isUpdated) {
    emit(
      "update",
      selectedValues.value.map((v) => v.value),
    )
  }
})
</script>

<style scoped lang="scss">
.v-input:deep(.v-field) {
  white-space: nowrap;
}

.v-input:deep(.v-input__details) {
  display: none;
}
</style>
