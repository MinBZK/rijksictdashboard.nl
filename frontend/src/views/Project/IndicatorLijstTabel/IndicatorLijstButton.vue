<template>
  <RidButton
    ref="button"
    variant="outlined"
    prepend-icon="mdi-magnify"
    @click="showIndicatorLijst = true"
    >Bekijk
    {{
      indicatorLijst?.IndicatorLijstMeervoudsNaamAlias.toLowerCase()
    }}</RidButton
  >
  <RidDialog
    v-if="
      showIndicatorLijst && indicatorLijst?.IndicatorLijstMeervoudsNaamAlias
    "
    :return-focus="button?.focus"
    max-width="1200"
    :title="indicatorLijst?.IndicatorLijstMeervoudsNaamAlias"
    @close="showIndicatorLijst = false"
  >
    <IndicatorLijstTabel :indicator-lijst="indicatorLijst" />
  </RidDialog>
</template>

<script setup lang="ts">
import type { IndicatorlijstNamen } from "@/api-new"
import type { IndicatorLijstMetAlias } from "@/composables/useIndicatorLijst"
import IndicatorLijstTabel from "./IndicatorLijstTabel.vue"
import RidButton from "@/components/RidButton.vue"
import RidDialog from "@/components/RidDialog.vue"

defineProps<{
  indicatorLijstNaam: IndicatorlijstNamen
  indicatorLijst?: IndicatorLijstMetAlias
}>()

const showIndicatorLijst = ref<boolean>(false)

const button = ref<typeof RidButton | null>(null)
</script>
