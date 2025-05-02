<template>
  <Page title="Rapportagegeschiedenis">
    <RidTable :table-data="rapportageGeschiedenis" :columns="columnConfig" />
  </Page>
</template>

<script setup lang="ts">
import { useContent } from "@/composables/useContent"
import Page from "@/components/Page.vue"
import RidTable from "@/components/RidTable.vue"
import type { TableConfig } from "@/types/table"

const { content } = useContent()

const rapportageGeschiedenis = computed(() => [
  ...content.rapportageGeschiedenis,
])

type ElementType<T> = T extends (infer U)[] ? U : T

type RowData = ElementType<typeof content.rapportageGeschiedenis>

const columnConfig: TableConfig<RowData>[] = [
  {
    key: "link",
    link: {
      label: "Bekijk JBR",
      variableColumn: "jaar",
    },
  },
  {
    key: "nummer",
    hidden: true,
  },
]
</script>
