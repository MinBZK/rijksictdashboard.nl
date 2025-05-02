<template>
  <v-col
    :cols="cols"
    :class="`py-0 ${marginBottomClass}`"
    :sm="sm"
    :lg="lg"
    :md="md"
  >
    <RidColCard v-bind="props">
      <template
        v-for="slot in [
          'default',
          'outside-wrapper-before',
          'outside-wrapper-after',
        ]"
        #[slot]
      >
        <router-link v-if="route && slot == 'default'" :key="slot" :to="route">
          <slot :name="slot" />
        </router-link>
        <slot v-if="slot !== 'default' || !route" :name="slot" />
      </template>
    </RidColCard>

    <slot name="card-after" />
  </v-col>
</template>

<script setup lang="ts">
import RidColCard from "./RidColCard.vue"
import type { RouteLocationRaw } from "vue-router"
import type { TitleLevel } from "@/types/components"

type RidCol = {
  title?: string
  cols?: number
  sm?: number
  lg?: number
  md?: number
  minContentHeight?: number
  fillHeight?: boolean
  img?: string
  imgTitle?: string
  imgMaxHeight?: number
  route?: RouteLocationRaw
  hasBorder?: boolean
  noPadding?: boolean
  titleInBar?: boolean
  subtitle?: string
  titleLevel?: TitleLevel
  marginBottomClass?: string
  imgCopyrightText?: string
}

const props = withDefaults(defineProps<RidCol>(), {
  cols: 12,
  hasBorder: true,
  marginBottomClass: "mb-4",
})
</script>

<style scoped lang="scss">
@media (min-width: 1264px) {
  .lg5-custom {
    flex: 0 0 20%;
    max-width: 20%;
  }
}

a.div:focus {
  outline: 2px dashed #000;
  z-index: 1010;
  outline-offset: 0;
  -webkit-box-shadow: 0 0 0 2px #fff;
  box-shadow: 0 0 0 2px #fff;
}
</style>
