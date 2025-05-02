<template>
  <TextLoaderContent content-group="ICT-medewerkers" content-field-key="Deel 1" />
  <TextLoaderContent
    content-group="ICT-medewerkers"
    content-field-key="Deel 2"
    title="Waarom is KWIV nodig?"
    :expandable="true"
  />
  <KwivGrafiek
    :jaar="2023"
    title="Actueel: aantal medewerkers met een KWIV-profiel per categorie"
  />
  <KwivGrafiek
    :jaar="2022"
    title="Aantal medewerkers met een KWIV-profiel per categorie en IV-inhuur"
  />
</template>

<script setup lang="ts">
import TextLoaderContent from "@/components/TextLoaderContent.vue"
import KwivGrafiek from "./ICTMedewerkers/KwivGrafiek.vue"
</script>
