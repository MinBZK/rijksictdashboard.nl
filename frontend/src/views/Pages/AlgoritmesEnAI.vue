<template>
  <TextLoaderContent content-group="Algoritmen" content-field-key="content" />
  <TextLoaderContent
    v-for="key in expandableContentKeys"
    :key="key"
    content-group="Algoritmen"
    :content-field-key="key"
    :title="key"
    :expandable="true"
  />
</template>

<script setup lang="ts">
import TextLoaderContent from "@/components/TextLoaderContent.vue"

const expandableContentKeys = [
  "Impactvolle algoritmes",
  "Openheid in Algoritmeregister",
  "Doelen Algoritmeregister",
  "Meer over verantwoord algoritmegebruik door de overheid",
]
</script>
