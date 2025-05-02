<template>
  <select v-model="selectedValue">
    <option v-for="i in items" :key="i" :value="i">{{ i }}</option>
  </select>
</template>

<script setup lang="ts">
const props = defineProps<{
  items: string[]
  modelValue?: string | null
}>()

const selectedValue = ref<string>(props.items[0])

const emit = defineEmits<{
  (e: "update:modelValue", newVal: string | null): void
}>()

watch(selectedValue, () => emit("update:modelValue", selectedValue.value))
</script>

<style scoped lang="scss">
select {
  padding: 0.5em 0.5em;
  appearance: auto !important;
  -webkit-appearance: auto !important;
  border: 1px solid black;
}
</style>
