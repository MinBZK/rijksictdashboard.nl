<template>
  <template v-if="Array.isArray(caption)">
    <p v-for="p in caption" :key="p" class="mb-4">
      {{ p }}
    </p>
  </template>
  <template v-else>
    <div class="mb-4" v-html="caption" />
  </template>
</template>

<script setup lang="ts">
defineProps<{
  caption: string[] | string
}>()
</script>

<style scoped lang="scss">
div :deep(ul) {
  padding-left: 1em;
}

div :deep(p) {
  padding-bottom: 1em !important;
}
</style>
