<template>
  <RidRow :title="title" :title-level="titleLevel">
    <v-col v-if="sliderData.length > 0">
      <v-slide-group show-arrows>
        <v-slide-group-item
          v-for="{
            title: sliderTitle,
            subtitle,
            route,
            subtitleRoute,
          } in sliderData"
          :key="sliderTitle"
        >
          <RidColCard
            :fill-height="true"
            :title-in-bar="false"
            width="250"
            class="mx-2 px-0"
          >
            <div class="card">
              <h3 class="smaller-text">
                <router-link v-if="route" :to="route" class="text-small">{{
                  sliderTitle
                }}</router-link>
              </h3>
              <span v-if="!route">{{ sliderTitle }}</span>
              <div class="mt-3 do-wrap">
                <template v-if="subtitleRoute">
                  <router-link
                    v-if="subtitleRoute"
                    :to="subtitleRoute"
                    class="black-link"
                  >
                    {{ subtitle }}
                  </router-link>
                </template>
                <template v-else>
                  {{ subtitle }}
                </template>
              </div>
            </div>
          </RidColCard>
        </v-slide-group-item>
      </v-slide-group>
    </v-col>
    <v-col v-else>Geen items gevonden.</v-col>
  </RidRow>
</template>

<script setup lang="ts">
import type { TileSliderData, TitleLevel } from "@/types/components"
import RidRow from "@/components/RidRow.vue"
import RidColCard from "./RidColCard.vue"

withDefaults(
  defineProps<{
    sliderData: TileSliderData[]
    title?: string
    titleLevel?: TitleLevel
  }>(),
  {
    sliderData: () => [],
  },
)
</script>

<style lang="scss" scoped>
@import "@/styles/main.scss";

.do-wrap {
  white-space: normal;
  overflow-wrap: normal !important;
  text-overflow: unset !important;
}

.card {
  height: 120px;
}

.smaller-text {
  font-size: 1.1rem;
}

.black-link {
  text-decoration: underline;
  color: black !important;
}
</style>
