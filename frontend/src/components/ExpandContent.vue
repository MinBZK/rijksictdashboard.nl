<template>
  <div class="mb-5 expand-container">
    <button
      class="full-width-button"
      tabindex="0"
      aria-role="button"
      :aria-expanded="expand ? 'true' : 'false'"
      @click="toggleExpand"
      @keyup.enter="toggleExpand"
      @keyup.space="toggleExpand"
    >
      <dynamic-heading
        :title-level="titleLevel"
        class="prevent-select expand-title"
      >
        <v-icon class="font-weight-regular">{{
          expand ? "mdi-chevron-up" : "mdi-chevron-down"
        }}</v-icon>
        {{ title }}
      </dynamic-heading>
    </button>
    <div :class="['text', expand && 'expanded']"><slot /></div>
  </div>
</template>

<script setup lang="ts">
import type { TitleLevel } from "@/types/components"
import DynamicHeading from "./DynamicHeading.vue"
const expand = ref<boolean>(false)

const props = withDefaults(
  defineProps<{
    title: string
    titleLevel?: TitleLevel
    autoExpand?: boolean
  }>(),
  {
    titleLevel: "h2",
    autoExpand: true,
  },
)

const title = toRef(props, "title")

watch(title, () => {
  if (props.autoExpand) expand.value = true
})

function toggleExpand() {
  expand.value = !expand.value
}
</script>

<style scoped>
.v-expansion-panel-title {
  font-size: 1.2em !important;
}

.full-width-button {
  width: 100%;
  cursor: pointer;
  padding: 0.8em 0.2em;
  border-radius: 3px;
  text-align: left !important;
}

.full-width-button:hover {
  background-color: #f0f0f0;
}

.expanded {
  display: inline !important;
}

.text {
  display: none;
}

h1,
h2,
h3,
h4 {
  margin-bottom: 0;
}

.prevent-select {
  -webkit-user-select: none; /* Safari */
  -ms-user-select: none; /* IE 10 and IE 11 */
  user-select: none; /* Standard syntax */
}

.expand-title {
  font-weight: bold;
  font-family: "RO Sans Bold", sans-serif !important;
  font-size: 1.2em;
}

.expand-container {
  width: 100%;
}
</style>
