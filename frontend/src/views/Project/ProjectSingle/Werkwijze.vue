<template>
  <RijksoverheidCard title="Werkwijze" :title-in-bar="true">
    <v-row class="mb-5">
      <RijksoverheidCardField
        v-for="indicator in ['Ontwikkelwijze', 'Maatwerk']"
        :key="indicator"
        :title="indicator"
      >
        <IndicatorLijstTabelWaarde
          :indicator="
            getFormulierWaarde(indicatorLijstAlgemeen?.Formulier[0], indicator)
          "
        />
      </RijksoverheidCardField>
    </v-row>
    <IndicatorLijstExpansion
      :project="project"
      :indicator-lijst-namen="indicatorLijstNamen"
    />
  </RijksoverheidCard>
</template>

<script setup lang="ts">
import RijksoverheidCard from "@/components/RidCol.vue"
import RijksoverheidCardField from "@/components/RidColField.vue"
import type {
  Formulier,
  ProjectMetAlleMetricsEnIndicatorLijsten,
} from "@/api-new"
import IndicatorLijstExpansion from "../IndicatorLijstTabel/IndicatorLijstExpansion.vue"
import IndicatorLijstTabelWaarde from "../IndicatorLijstTabel/IndicatorLijstTabelWaarde.vue"
import { useIndicatorLijst } from "@/composables/useIndicatorLijst"
import { IndicatorlijstNamen } from "@/api-new"

const props = defineProps<{
  project: ProjectMetAlleMetricsEnIndicatorLijsten
}>()

const project = toRef(props, "project")

const { getIndicatorLijst } = useIndicatorLijst(project)

const indicatorLijstAlgemeen = computed(() =>
  getIndicatorLijst(IndicatorlijstNamen.ALGEMEEN),
)

const getFormulierWaarde = (
  formulier: Formulier | undefined,
  indicatorTitel: string,
) => {
  return formulier
    ? formulier.FormulierWaardes.find(
        (fW) => fW.IndicatorTitel == indicatorTitel,
      )
    : undefined
}

const indicatorLijstNamen: IndicatorlijstNamen[] = [
  IndicatorlijstNamen.ONTWIKKELPARTIJEN,
  IndicatorlijstNamen.BEHEER,
]
</script>
