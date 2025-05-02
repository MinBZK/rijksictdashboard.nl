<template>
  <div
    :class="{
      'mb-5': !noBottomPadding,
    }"
  >
    <v-col v-if="allowHide" class="pt-0 px-0">
      <div
        v-if="title || allowHide"
        class="text-primary mt-2"
        :class="alignToggleLabel == 'right' && 'text-right'"
      >
        <div
          tabindex="0"
          class="d-inline"
          :aria-label="showMoreLabel"
          :title="showMoreLabel"
          :aria-expanded="showContent ? 'true' : 'false'"
          role="button"
          @click="showContent = !showContent"
          @keydown.enter="showContent = !showContent"
          @keydown.space="showContent = !showContent"
        >
          <span rounded="0" class="link">{{
            showContent ? showLessLabel : showMoreLabel
          }}</span
          ><v-icon :icon="`mdi-chevron-${showContent ? 'up' : 'down'}`" />
        </div>
      </div>
    </v-col>

    <div
      :class="{
        'mb-5': !noBottomPadding,
      }"
    >
      <dynamic-heading
        v-if="showTitle"
        :title-level="titleLevel"
        :class="titleClass"
        :aria-label="ariaLabel"
      >
        {{ title }}</dynamic-heading
      >
      <p v-if="caption !== undefined" class="pb-1" v-html="caption" />
      <v-row
        v-if="showContent"
        :class="allowHide && 'bg-accent2'"
        :align="center ? 'center' : undefined"
        class="rid-row"
      >
        <slot />
      </v-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { TitleLevel } from "@/types/components"
import DynamicHeading from "./DynamicHeading.vue"

const props = withDefaults(
  defineProps<{
    title?: string
    smallTitle?: boolean
    additionalBottomPaddingUnits?: number
    allowHide?: boolean
    showMoreLabel?: string
    showLessLabel?: string
    noBottomPadding?: boolean
    caption?: string
    alignToggleLabel?: "left" | "right"
    titleLevel?: TitleLevel
    center?: boolean
    ariaLabel?: string
    manualExpand?: boolean
  }>(),
  {
    allowHide: false,
    showMoreLabel: "Meer informatie",
    showLessLabel: "Verbergen",
    noBottomPadding: false,
    smallTitle: false,
    manualExpand: false,
    alignToggleLabel: "right",
    titleLevel: "h2",
    center: false,
  },
)

const showContent = ref<Boolean>(
  props.allowHide || props.manualExpand ? false : true,
)

const titleClass = computed(() => [
  props.caption ? "mb-2" : "mb-1",
  {
    "small-title": props.smallTitle,
  },
])

const showTitle = computed(() => props.title && !props.allowHide)
</script>

<style scoped lang="scss">
@import "@/styles/main.scss";
.link {
  cursor: pointer;
}

.small-title {
  font-size: 1em !important;
}

.rid-row {
  margin-top: 0;
}

p :deep(ul) {
  padding-left: 2em;
}
</style>
