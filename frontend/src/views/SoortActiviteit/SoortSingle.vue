<template>
  <AttributeDetail
    attribute="SoortICTActiviteit"
    attribute-label="Soort ICT-activiteit"
    :attribute-value="soort"
  >
  </AttributeDetail>
</template>

<script setup lang="ts">
import AttributeDetail from "@/views/AttributeDetail.vue"

defineProps<{
  soort: string
}>()
</script>
