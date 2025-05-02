<template>
  <AttributeDetail
    attribute="Dienstverlening"
    :attribute-value="dienstverlening"
    attribute-label="Dienstverlening"
  >
    <p v-if="dienstverleningUrls[props.dienstverlening]" class="mb-5">
      <a
        :href="`${baseUrl}${dienstverleningUrls[props.dienstverlening]}`"
        target="_blank"
        rel="noopener"
        >Bekijk deze dienstverlening op de website van de Rijksoverheid</a
      >
    </p>
  </AttributeDetail>
</template>

<script setup lang="ts">
import AttributeDetail from "@/views/AttributeDetail.vue"
import dienstverleningUrls from "@/content/dienstverlening"

const props = defineProps<{
  dienstverlening: string
}>()

const baseUrl = "https://www.rijksoverheid.nl"
</script>
