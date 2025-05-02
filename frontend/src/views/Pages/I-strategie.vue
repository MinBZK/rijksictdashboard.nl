<template>
  <TextLoaderContent content-group="I-strategie" content-field-key="Deel 1" />
  <TextLoaderContent
    content-group="I-strategie"
    content-field-key="Deel 2"
    title="Meer informatie"
    :expandable="true"
  />
</template>

<script setup lang="ts">
import TextLoaderContent from "@/components/TextLoaderContent.vue"
</script>
