<template>
  <div class="p-float-label">
    <PrimeMultiSelect
      v-model="selectedValues"
      :options="calculatedItems"
      :option-label="itemLabelKey"
      class="full-width"
      show-clear
      :input-id="id"
      scroll-height="300px"
      empty-message="Geen opties beschikbaar"
      :disabled="calculatedItems.length == 0"
    >
      <template #value>
        {{ selectedValues.length }}
        {{ selectedValues.length == 1 ? "optie" : "opties" }} geselecteerd
      </template>
    </PrimeMultiSelect>
    <label :for="id">{{ label }}</label>
  </div>
</template>

<script setup lang="ts">
import type { ItemSelect } from "@/types/components"

const id = `select-${(Math.random() + 1).toString(36).substring(7)}`

const props = defineProps<{
  items: ItemSelect[]
  itemLabelKey: keyof ItemSelect
  itemValueKey: keyof ItemSelect
  modelValue: ItemSelect[]
  label: string
}>()

const modelValue = toRef(props, "modelValue")

const calculatedItems = computed(() => {
  return props.items.map((item) => {
    if (item[props.itemLabelKey].length == 0) {
      item[props.itemLabelKey] = "(niet ingevuld)"
    }
    return item
  })
})

const selectedValues = ref<ItemSelect[]>([])

const emit = defineEmits<{
  (e: "update:modelValue", v: ItemSelect[]): void
}>()

watch(selectedValues, () => {
  emit("update:modelValue", selectedValues.value)
})

watch(
  modelValue,
  () => {
    if (
      JSON.stringify(selectedValues.value.map((v) => v["value"])) !==
      JSON.stringify(modelValue.value.map((v) => v["value"]))
    ) {
      selectedValues.value = modelValue.value
    }
  },
  {
    immediate: true,
    deep: true,
  },
)
</script>

<style scoped>
label {
  font-size: 0.9em;
  color: unset !important;
}
</style>
