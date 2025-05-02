<template>
  <Page title="Versie-informatie" :text-only="true">
    <TextLoaderContent
      content-group="Release notes"
      content-field-key="content"
    />
  </Page>
</template>

<script setup lang="ts">
import Page from "@/components/Page.vue"
import TextLoaderContent from "@/components/TextLoaderContent.vue"
</script>
