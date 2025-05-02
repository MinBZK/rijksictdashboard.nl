<template>
  <template v-if="route">
    <router-link :to="route">
      {{ finalValue }}
    </router-link>
  </template>
  <template v-else-if="typeof finalValue === 'string'">
    <template v-if="scrollDivId">
      <a
        aria-label="Scroll naar het onderdeel met meer informatie hierover"
        @click="scrollToDivId(scrollDivId)"
        @keydown.enter="scrollToDivId(scrollDivId)"
        ><FormattedValueMultilineString :value="finalValue"
      /></a>
    </template>
    <template v-else
      ><FormattedValueMultilineString :value="finalValue"
    /></template>
  </template>
  <template v-else>
    {{ finalValue }}
  </template>

  <ButtonIcon
    v-if="hasDifferentShortValue"
    ref="expandButton"
    icon="mdi-arrow-expand-all"
    aria-label="Toon volledige tekst"
    @click="showExpandedValue = !showExpandedValue"
    @keydown.enter.prevent="showExpandedValue = !showExpandedValue"
    @keydown.space="showExpandedValue = !showExpandedValue"
  />
  <RidDialog
    v-if="showExpandedValue"
    :content="formattedValue"
    :activator="expandButton"
    :title="valueTitle"
    :return-focus="expandButton?.focus"
    @close="showExpandedValue = false"
  />
</template>

<script setup lang="ts">
import ButtonIcon from "@/components/ButtonIcon.vue"
import { formatValue, type FormatConfig } from "@/util"
import type { RouteLocationRaw } from "vue-router"
import FormattedValueMultilineString from "./FormattedValueMultilineString.vue"
import RidDialog from "./RidDialog.vue"

const props = withDefaults(
  defineProps<{
    value?: string | number | null
    maxWords?: number
    valueTitle?: string
    route?: RouteLocationRaw
    minDigits?: number
    maxDigits?: number
    unitSuffix?: string
    formatConfig: FormatConfig
    scrollDivId?: string
  }>(),
  { value: "", maxWords: 20, valueTitle: "" },
)

const formattedValue = computed(() =>
  formatValue(props.value, props.formatConfig),
)

const showExpandedValue = ref<boolean>(false)

const shortValue = computed(() => {
  const maxWords = props.maxWords
  if (typeof formattedValue.value == "string") {
    const shortString = formattedValue.value
      .split(" ")
      .splice(0, maxWords)
      .join(" ")
    return shortString.length < formattedValue.value.length
      ? shortString
      : formattedValue.value
  } else {
    return formattedValue.value
  }
})

const hasDifferentShortValue = computed(() => {
  if (
    typeof formattedValue.value == "string" &&
    typeof shortValue.value == "string"
  ) {
    return shortValue.value.length !== formattedValue.value.length
  } else {
    return false
  }
})

const finalValue = computed(() => {
  return hasDifferentShortValue.value
    ? shortValue.value + "..."
    : formattedValue.value || "-"
})

const expandButton = ref<typeof ButtonIcon | null>(null)

const scrollToDivId = (id: string) => {
  const el = document.getElementById(id)
  if (el) {
    el.scrollIntoView({ behavior: "smooth" })
  }
}
</script>

<style scoped lang="scss">
@import "@/styles/_colors.scss";

span {
  font-size: 0.8em;
}

a {
  cursor: pointer;
}
</style>
