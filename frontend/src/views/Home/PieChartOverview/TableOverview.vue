<script setup lang="ts">
import type { ProjectMetCoreMetrics } from "@/api-new/models/ProjectMetCoreMetrics"
import type { TableConfig } from "@/types/table"

defineProps<{
  projecten: ProjectMetCoreMetrics[]
}>()

const columnConfig: TableConfig<ProjectMetCoreMetrics>[] = [
  {
    key: "Naam",
    label: "Naam",
    formatInSlot: true,
  },
  {
    key: "MinisterieNaam",
    label: "Ministerie",
  },
  {
    key: "SoortICTActiviteit",
    label: "Soort",
  },
  {
    key: "SchattingTotaleKostenHuidigJaar",
    label: "Geschatte totale kosten",
    dataType: "currency-million",
  },
]
</script>

<template>
  <RidTable
    v-if="projecten"
    :table-data="projecten"
    :columns="columnConfig"
    :column-sequence="[
      'Naam',
      'MinisterieNaam',
      'SoortICTActiviteit',
      'SchattingTotaleKostenHuidigJaar',
    ]"
  >
    <template #custom-table-cell="{ cellData: project }">
      <router-link
        :to="{
          name: 'ict-activiteit',
          params: { projectId: project.ProjectId, slug: project.Slug },
        }"
      >
        {{ project.Naam }}</router-link
      >
    </template>
  </RidTable>
</template>
