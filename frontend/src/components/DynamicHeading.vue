<template>
  <h1 v-if="titleLevel == 'h1'"><slot /></h1>
  <h2 v-else-if="titleLevel == 'h2'"><slot /></h2>
  <h3 v-else-if="titleLevel == 'h3'"><slot /></h3>
  <h4 v-else-if="titleLevel == 'h4'"><slot /></h4>
</template>

<script setup lang="ts">
import type { TitleLevel } from "@/types/components"

defineProps<{
  titleLevel: TitleLevel
}>()
</script>
