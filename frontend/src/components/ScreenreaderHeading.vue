<template>
  <p role="heading" :aria-level="headingLevel" class="sr-only">{{ title }}</p>
  <p v-if="description" class="sr-only">
    Schermlezerinformatie: {{ description }}
  </p>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  description?: string
  headingLevel: "1" | "2" | "3" | "4"
}>()
</script>
