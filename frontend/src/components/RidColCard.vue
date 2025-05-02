<template>
  <v-card
    variant="outlined"
    :class="[
      'rounded-0',
      {
        'fill-height': fillHeight,
        'col-border': hasBorder,
        'no-border': !hasBorder,
      },
    ]"
  >
    <v-toolbar v-if="title && titleInBar" class="toolbar" color="tertiary">
      <h2 v-if="titleLevel == 'h2'" class="mb-0">{{ title }}</h2>
      <h3 v-if="titleLevel == 'h3'" class="mb-0">{{ title }}</h3>
    </v-toolbar>
    <slot name="outside-wrapper-before" />

    <router-link
      v-if="route"
      :to="route"
      tabindex="-1"
      :aria-hidden="hideImgForScreenreader ? 'true' : 'false'"
    >
      <v-img
        v-if="img"
        :max-height="imgMaxHeight"
        :cover="true"
        :src="img"
        :title="imgTitle"
        :alt="imgTitle"
        ><div v-if="imgCopyrightText" class="copyright">
          {{ imgCopyrightText }}
        </div></v-img
      >
    </router-link>

    <v-img
      v-if="img && !route"
      :max-height="imgMaxHeight"
      :cover="true"
      :src="img"
      :title="imgTitle"
      :alt="imgTitle"
      :aria-hidden="hideImgForScreenreader ? 'true' : 'false'"
      ><div v-if="imgCopyrightText" class="copyright">
        {{ imgCopyrightText }}
      </div></v-img
    >
    <v-card-text :class="noPadding ? 'pa-0' : 'px-4'">
      <template v-if="!titleInBar && title">
        <h3 v-if="titleLevel == 'h3'" :class="'pb-4' && !subtitle">
          {{ title }}
        </h3>
        <h2 v-if="titleLevel == 'h2'" :class="'pb-4' && !subtitle">
          {{ title }}
        </h2>
      </template>

      <p v-if="subtitle" class="pb-4 text-subtitle-2" v-html="subtitle" />
      <slot />
    </v-card-text>
    <slot name="outside-wrapper-after" />
  </v-card>
</template>

<script setup lang="ts">
import type { RouteLocationRaw } from "vue-router"
import type { TitleLevel } from "@/types/components"

// copy pasted from RidCol.vue, for some reason it can't be imported from an external file, even though the Vue docs state this should work
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

withDefaults(defineProps<RidCol>(), {
  imgMaxHeight: 200,
  fillHeight: false,
  hasBorder: true,
  titleInBar: true,
  titleLevel: "h2",
})

const hideImgForScreenreader = ref<boolean>(true)
</script>

<style scoped lang="scss">
@import "@/styles/colors.scss";
.v-card-text {
  font-size: 1.1rem !important;
}

.toolbar {
  font-size: 90%;
  padding-left: 1.5rem;
}

.v-card:deep(.v-card-title) {
  white-space: normal !important;
  font-size: 0.95em;
}

.v-card:deep(.v-card-text) {
  white-space: normal !important;
  font-size: 1em;
}

.col-border {
  border: 1px solid $tertiary;
}

.no-border {
  border: 0;
}

.copyright {
  position: absolute;
  z-index: 10;
  bottom: 0.25rem;
  left: 0.5rem;
  margin: 0;
  color: #fff;
  font-size: 0.7em;
  text-shadow:
    0px 0px 1px rgba(0, 0, 0, 0.5),
    -1px 0px 1px rgba(0, 0, 0, 0.5),
    1px 0px 1px rgba(0, 0, 0, 0.5),
    0px -1px 1px rgba(0, 0, 0, 0.5),
    0px 1px 1px rgba(0, 0, 0, 0.5),
    2px 2px 6px rgba(0, 0, 0, 0.5);
}
</style>
