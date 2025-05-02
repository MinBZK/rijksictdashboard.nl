<template>
  <tr :class="expandRow && 'expanded-row'">
    <td v-if="hiddenFields.length > 0">
      <ButtonIcon
        aria-label="Toon meer informatie over deze rij"
        role="button"
        :aria-expanded="expandRow ? 'true' : 'false'"
        :icon="`mdi-arrow-${expandRow ? 'down' : 'right'}-drop-circle-outline`"
        @click="expandRow = !expandRow"
        @keyup.enter="expandRow = !expandRow"
        @keyup.space="expandRow = !expandRow"
      />
    </td>
    <IndicatorLijstTabelCel
      v-for="h in headers"
      :key="h"
      :indicator="
        formulier.FormulierWaardes.find((fW) => fW.IndicatorTitel == h)
      "
      :value-is-url="valueIsUrl(h)"
      :always-align-left="true"
    />
  </tr>
  <tr v-if="expandRow">
    <td :colspan="headers.length + 1">
      <slot />
    </td>
  </tr>
</template>

<script setup lang="ts">
import IndicatorLijstTabelCel from "./IndicatorLijstTabelCel.vue"
import ButtonIcon from "@/components/ButtonIcon.vue"
import type { Formulier } from "@/api-new"

const props = defineProps<{
  formulier: Formulier
  headers: string[]
  urlFields: string[]
  hiddenFields: string[]
}>()

const valueIsUrl = (header: string) => {
  return (props.urlFields || []).includes(header)
}

const expandRow = ref<Boolean>(false)

watch(props, () => {
  expandRow.value = false
})
</script>

<style lang="scss" scoped>
@import "@/styles/_colors.scss";

tr.expanded-row td {
  border-bottom: 0 !important;
}

th {
  text-align: left !important;
}

.icon-button:hover {
  color: $primary;
}
</style>
