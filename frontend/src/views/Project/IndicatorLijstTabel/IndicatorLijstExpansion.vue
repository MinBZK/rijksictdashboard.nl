<template>
  <v-expansion-panels v-for="naam in indicatorLijstNamen" :key="naam" multiple>
    <v-expansion-panel
      class="custom-panel"
      rounded="0"
      elevation="0"
      bg-color="white"
    >
      <v-expansion-panel-title :aria-label="naam">
        {{ naam }}

        <template v-if="!getIndicatorLijst(naam)?.IndicatorLijstEnkelFormulier"
          >({{
            getIndicatorLijst(naam)?.FormulierGefilterd.length || 0
          }})</template
        >
      </v-expansion-panel-title>
      <v-expansion-panel-text
        ><IndicatorLijstTabel :indicator-lijst="getIndicatorLijst(naam)" />
      </v-expansion-panel-text>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script setup lang="ts">
import IndicatorLijstTabel from "./IndicatorLijstTabel.vue"
import type {
  IndicatorlijstNamen,
  ProjectMetAlleMetricsEnIndicatorLijsten,
} from "@/api-new"
import { useIndicatorLijst } from "@/composables/useIndicatorLijst"

const props = defineProps<{
  indicatorLijstNamen: IndicatorlijstNamen[]
  project: ProjectMetAlleMetricsEnIndicatorLijsten
}>()

const project = toRef(props, "project")

const { getIndicatorLijst } = useIndicatorLijst(project)
</script>
<style scoped lang="scss">
@import "@/styles/_colors.scss";

.v-expansion-panel-title {
  font-size: 1.2em !important;
}
.custom-panel {
  border-bottom: 1px solid $grijs4;
  border-radius: 5px;
}

.v-expansion-panel-title:focus {
  outline: 2px dashed black;
  outline-offset: 4px;
}
</style>
