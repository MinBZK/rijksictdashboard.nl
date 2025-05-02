<template>
  <RidRow title="Top 3 recente ICT-activiteiten" class="mt-5">
    <RidCol
      v-for="listConfig in ToplistsConfig"
      :key="listConfig.listName"
      :lg="6"
      :sm="6"
      :cols="12"
    >
      <RidList
        :numbered="true"
        :config="listConfig"
        :data="metrics?.projecten[listConfig.listName] ?? []"
        :link-config="{
          name: 'ict-activiteit',
          routeIdKey: 'projectId',
          idKey: 'ProjectId',
        }"
      />
    </RidCol>
  </RidRow>
</template>

<script setup lang="ts">
import { useMetrics } from "@/composables/useMetrics"
import { useTextLoader } from "@/composables/useTextLoader"
import type { ListConfig } from "@/types/project"
import type { Project } from "@/api-new/"

const { getContent } = useTextLoader()

const { metrics } = useMetrics({
  statusType: "allActive",
})

const ToplistsConfig: ListConfig<Project>[] = [
  {
    listName: "Top 3 recent toegevoegde ICT-activiteiten",
    label: "Toegevoegd",
    caption: getContent("Dashboard", "ToelichtingTop3ToegevoegdeActiviteiten")
      .value,
    attributes: [
      { item: "Naam", type: "string" },
      { item: "ProjectVersieWijzigingsDatum", type: "date" },
    ],
  },
  {
    listName: "Top 3 recent afgeronde ICT-activiteiten",
    label: "Afgerond",
    caption: getContent("Dashboard", "ToelichtingTop3AfgerondeActiviteiten")
      .value,
    attributes: [
      { item: "Naam", type: "string" },
      { item: "ProjectVersieWijzigingsDatum", type: "date" },
    ],
  },
]
</script>
