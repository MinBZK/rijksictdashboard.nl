<template>
  <v-text-field
    ref="textField"
    variant="outlined"
    append-inner-icon="mdi-magnify"
    flat
    :label="labelAndPlaceholder"
    :single-line="true"
    :clearable="clearable"
    :placeholder="labelAndPlaceholder"
    :loading="loading"
    bg-color="white"
    rounded="0"
  >
    <template #loader>
      <v-progress-linear
        :active="loading"
        :color="'primary'"
        height="5"
        indeterminate
      ></v-progress-linear>
    </template>
  </v-text-field>
</template>

<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    labelAndPlaceholder: string
    clearable?: boolean
    isSearchBar?: boolean
    loading?: boolean
  }>(),
  {
    clearable: false,
    isSearchBar: false,
    loading: false,
  },
)
const textField = ref<HTMLElement | null>(null)

const getParents = (el: HTMLElement, levels: number) => {
  const parents: HTMLElement[] = el.parentElement ? [el.parentElement] : []
  if (levels > 0 && el.parentElement) {
    const newParents = getParents(el.parentElement, levels - 1)
    parents.push(...newParents)
  }
  return parents
}

watch(
  textField,
  () => {
    if (textField.value) {
      const nodes = getParents(textField.value, 1)
      nodes.forEach((node) => {
        if (!node.ariaLabel) node.ariaLabel = props.labelAndPlaceholder
        if (
          node instanceof HTMLElement &&
          node.getAttribute("role") === "textbox" &&
          props.isSearchBar
        ) {
          node.setAttribute("type", "search")
        }
      })
    }
  },
  { immediate: true },
)
</script>
