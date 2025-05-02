<template>
  <td
    :class="[
      isNumber && !alwaysAlignLeft && 'text-right',
      {
        'no-wrap': isDate,
      },
    ]"
  >
    <IndicatorLijstTabelWaarde
      :indicator="indicator"
      :value-is-url="valueIsUrl"
    />
  </td>
</template>

<script setup lang="ts">
import IndicatorLijstTabelWaarde from "./IndicatorLijstTabelWaarde.vue"
// import type { IndicatorWaarde } from "@/types/indicatorlijst"
import type { FormulierWaarde } from "@/api-new"

const props = withDefaults(
  defineProps<{
    indicator?: FormulierWaarde
    valueIsUrl?: boolean
    alwaysAlignLeft?: boolean
  }>(),
  {
    valueIsUrl: false,
    alwaysAlignLeft: false,
  },
)

const isDate = computed(
  () => props.indicator?.IndicatorAntwoordTypeNaam == "Datum",
)

const isNumber = computed(() => {
  const val = props.indicator?.Waarde
  if (val) {
    const float = parseFloat(val)
    return !isNaN(float) && !isDate.value
  } else {
    return false
  }
})
</script>

<style scoped lang="scss">
@import "@/styles/_variables.scss";
.no-wrap {
  white-space: nowrap;
}

.v-table > .v-table__wrapper > table > tbody > tr > td {
  font-size: $table-font-size !important;
}
</style>
