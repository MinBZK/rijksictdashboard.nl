<template>
  <TextLoaderContent
    content-group="Duurzaamheid"
    content-field-key="Content zonder projecten"
  />
  <TextLoaderContent
    v-for="key in expandableContentKeys"
    :key="key"
    content-group="Duurzaamheid"
    :content-field-key="key"
    :title="key"
    :expandable="true"
  />
  <GrafiekInfrastructuurEfficiency />
  <TextLoaderContent
    content-group="Duurzaamheid"
    content-field-key="content_deel2"
  />
</template>

<script setup lang="ts">
import TextLoaderContent from "@/components/TextLoaderContent.vue"
import GrafiekInfrastructuurEfficiency from "@/views/Duurzaamheid/GrafiekInfrastructuurEfficiency.vue"

const expandableContentKeys = [
  "Verminderen dubbele devices",
  "Verminderen dataopslag",
  "Bewustwording van gedrag",
  "Efficiënt opslaan",
  "Innovatie van datacentra",
]
</script>
