<template>
  <RidCol :no-padding="true" :has-border="false">
    <div class="bar">
      <v-col :cols="12" :lg="2" class="bg-primary px-7 py-4"
        ><h3 class="no-margin">
          <span class="laatst-aangepast">Laatst aangepast</span>
        </h3></v-col
      >
      <v-col :cols="12" :lg="10" class="bg-quaternary px-8 py-6">
        <p v-if="mostRecent">
          <strong
            ><FormattedValue
              :value="mostRecent?.ProjectVersieWijzigingsDatum"
              :format-config="{ dataType: 'date' }"
          /></strong>

          De activiteit
          <router-link
            :to="{
              name: 'ict-activiteit',
              params: {
                projectId: mostRecent.ProjectId,
                slug: mostRecent.Slug,
              },
            }"
            >{{ mostRecent.Naam }}</router-link
          >
          van
          <router-link
            :to="{
              name: 'ministerie',
              params: {
                attributeValue: mostRecent?.MinisterieNaam,
              },
            }"
            >{{ mostRecent?.MinisterieNaam }}</router-link
          >
          is aangepast.
        </p>
      </v-col>
    </div>
  </RidCol>
</template>

<script setup lang="ts">
import FormattedValue from "@/components/FormattedValue.vue"
import RidCol from "@/components/RidCol.vue"
import { useLastChanged } from "@/composables/useLastChanged"

const props = defineProps<{
  ministerie?: string
}>()

const ministerie = toRef(props, "ministerie")

const { projecten } = useLastChanged(ministerie)

const mostRecent = computed(() => projecten.value[0])
</script>

<style scoped lang="scss">
div.bar {
  display: flex;
  flex-wrap: wrap;
}
.laatst-aangepast {
  font-size: 1.1rem;
}

.no-margin {
  margin: 0;
}
</style>
