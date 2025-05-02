<template>
  <TextLoaderContent
    :content-group="contentGroup"
    :content-field-key="contentKey"
  />
</template>

<script setup lang="ts">
import TextLoaderContent from "@/components/TextLoaderContent.vue"

defineProps<{
  contentGroup: string
  contentKey: string
}>()
</script>
