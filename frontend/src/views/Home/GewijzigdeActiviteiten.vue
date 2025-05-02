<template>
  <div v-for="(item, index) in projecten.slice(0, 5)" :key="index" class="mb-4">
    <p class="blue-text smaller mb-1">
      <router-link
        :to="{
          name: 'ict-activiteit',
          params: { projectId: item.ProjectId, slug: item.Slug },
        }"
      >
        <h4 class="no-margin smaller-text">
          {{ item.Naam }}
        </h4></router-link
      >
    </p>
    <p class="font-weight-bold text-body-2 mb-1">
      <FormattedValue
        :format-config="{ dataType: 'date' }"
        :value="item.ProjectVersieWijzigingsDatum"
      />
    </p>
    <p class="text-body-2">{{ item.MinisterieNaam }}</p>
  </div>
</template>

<script setup lang="ts">
import FormattedValue from "@/components/FormattedValue.vue"
import { useLastChanged } from "@/composables/useLastChanged"

const props = defineProps<{
  ministerie?: string
}>()

const ministerie = toRef(props, "ministerie")

const { projecten } = useLastChanged(ministerie)
</script>

<style scoped lang="scss">
@import "@/styles/main.scss";
.smaller-text {
  font-size: 1rem;
}
</style>
