<template>
  <Page title="Pagina niet gevonden" :min-height="300"
    ><p>
      Deze pagina bestaat niet.
      <router-link :to="{ name: 'home' }"
        >Ga terug naar de homepagina.</router-link
      >
    </p></Page
  >
</template>

<script setup lang="ts">
import Page from "@/components/Page.vue"
</script>
