<template>
  <Page title="Privacy" :text-only="true">
    <TextLoaderContent
      content-field-key="content"
      content-group="Privacyverklaring"
    />
  </Page>
</template>

<script setup lang="ts">
import Page from "@/components/Page.vue"
import TextLoaderContent from "@/components/TextLoaderContent.vue"
</script>
