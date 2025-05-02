<template>
  <div class="p-float-label mt-4 mb-2">
    <PrimeDropdown
      v-model="selectedValue"
      :options="calculatedItems"
      option-label="title"
      :input-id="id"
      :placeholder="label"
      :aria-label="label"
      class="full-width"
      scroll-height="300px"
    >
    </PrimeDropdown>
    <label :for="id">{{ label }}</label>
  </div>
</template>

<script setup lang="ts">
import type { ItemSelect } from "@/types/components"

const props = withDefaults(
  defineProps<{
    items: ItemSelect[]
    label: string
    allowNone?: boolean
    selectNoneLabel?: string
    modelValue?: string | number | null
  }>(),
  {
    allowNone: false,
    selectNoneLabel: "Verwijder selectie",
  },
)

const calculatedItems = computed(() => {
  if (props.allowNone) {
    const noneItem: ItemSelect = {
      title: props.selectNoneLabel,
      value: props.selectNoneLabel,
    }
    return [noneItem, ...props.items]
  } else {
    return props.items
  }
})

const selectedValue = ref<ItemSelect | null>(null)
const selectedValueIndex = computed(() => {
  return selectedValue.value
    ? calculatedItems.value
        .map((i) => i.title)
        .indexOf(selectedValue.value.title)
    : -1
})

const id = `dd-${(Math.random() + 1).toString(36).substring(7)}`

const emit = defineEmits<{
  (e: "update:modelValue", newVal: string | number | null | undefined): void
}>()

watch(selectedValue, () => {
  if (selectedValueIndex.value == 0 && props.allowNone) {
    selectedValue.value = null
  } else {
    const newValue = selectedValue.value
      ? selectedValue.value.value
      : selectedValue.value
        ? selectedValue.value
        : null
    emit("update:modelValue", newValue)
  }
})

// two-way binding (from props)
const modelValue = toRef(props, "modelValue")
watch(
  modelValue,
  () => {
    const selectedItem = calculatedItems.value.find(
      (i) => i.value == modelValue.value,
    )
    if (selectedItem) selectedValue.value = selectedItem
  },
  { immediate: true },
)
</script>

<style scoped>
label {
  font-size: 0.9em;
  color: unset !important;
}
</style>
