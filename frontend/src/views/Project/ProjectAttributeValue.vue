<template>
  <template v-if="dataType == 'list'">
    <p v-for="(paragraph, index) in value" :key="index">
      {{ paragraph }}
    </p>
  </template>

  <template v-else>
    {{ displayedValue }}
    <span v-if="!displayedValue" class="sr-only">Geen waarde</span></template
  >
</template>

<script setup lang="ts">
import type { ProjectAttributePrimitiveDataType } from "@/types/project"
import { dateToLocaleDateString } from "@/util"

const props = defineProps<{
  dataType: ProjectAttributePrimitiveDataType
  value?: string | number | Array<string>
}>()

const displayedValue = computed(() => {
  if (props.dataType == "currency" && typeof props.value == "number") {
    return (
      new Intl.NumberFormat("nl-NL", {
        style: "currency",
        currency: "EUR",
      }).format(props.value * 1e-6) + " mln"
    )
  } else if (props.dataType == "date" && typeof props.value == "string") {
    return dateToLocaleDateString(new Date(Date.parse(props.value)))
  } else {
    return props.value
  }
})
</script>
