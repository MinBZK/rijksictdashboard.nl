<template>
  <div>
    <div
      v-if="!expandable"
      :class="['rich-content', smallText ? 'small-text' : '']"
      v-html="getContent(contentGroup, contentFieldKey).value"
    />
    <ExpandContent v-if="expandable && title !== undefined" :title="title"
      ><div
        :class="['rich-content', smallText ? 'small-text' : '']"
        v-html="getContent(contentGroup, contentFieldKey).value"
    /></ExpandContent>
  </div>
</template>

<script setup lang="ts">
import { useTextLoader } from "@/composables/useTextLoader"
import ExpandContent from "@/components/ExpandContent.vue"

const { getContent } = useTextLoader()

const props = withDefaults(
  defineProps<{
    smallText?: boolean
    contentGroup: string
    contentFieldKey: string
    title?: string
    expandable?: boolean
  }>(),
  {
    smallText: true,
    expandable: false,
  },
)

const expandable = toRef(props, "expandable")

watch(expandable, () => {
  if (expandable.value && props.title === undefined) {
    console.error("A title is required when expandable is set to true")
  }
})
</script>

<style scoped lang="scss">
.rich-content :deep(p) {
  margin-bottom: 0.75em;
}

.small-text {
  max-width: 800px;
}

.rich-content :deep(ol),
.rich-content :deep(ul) {
  margin-bottom: 1em;
}

.rich-content :deep(a:before) {
  display: inline-flex;
  align-items: center;
  left: 1px;
  top: 0;
  height: 22.4px;
}

.rich-content :deep(li) {
  margin-left: 1.5em;
}
</style>
