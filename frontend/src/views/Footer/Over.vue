<template>
  <Page title="Over" :text-only="true">
    <TextLoaderContent content-group="Over" content-field-key="deel1" />
    <TextLoaderContent content-group="Over" content-field-key="deel2" />
  </Page>
</template>

<script setup lang="ts">
import Page from "@/components/Page.vue"
import TextLoaderContent from "@/components/TextLoaderContent.vue"
</script>

<style scoped lang="scss">
@import "@/styles/main.scss";
.select-text {
  color: $primaryDark;
  font-size: 0.9em;
}
</style>
