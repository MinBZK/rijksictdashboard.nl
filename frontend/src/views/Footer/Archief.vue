<template>
  <Page title="Archief" :text-only="true">
    <TextLoaderContent content-group="Archief" content-field-key="content" />
  </Page>
</template>

<script setup lang="ts">
import Page from "@/components/Page.vue"
import TextLoaderContent from "@/components/TextLoaderContent.vue"
</script>

<style scoped lang="scss">
@import "@/styles/main.scss";
</style>
