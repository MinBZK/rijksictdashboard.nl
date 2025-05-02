<template>
  <v-table>
    <tbody>
      <tr>
        <th
          v-for="(h, index) in tableHeaders"
          :key="h"
          :class="index > 0 && 'px-6 text-right'"
          scope="column"
        >
          {{ h }}
        </th>
      </tr>
      <tr v-for="row in tableData" :key="row.Kosten">
        <td
          v-for="h in tableHeaders"
          :key="h"
          :class="[
            row.Kosten == 'Totaal' && 'cell-total',
            'pr-10',
            h != 'Kosten' && 'text-right px-6',
          ]"
        >
          <template v-if="h == 'Kosten'">{{ row[h] }}</template>
          <template v-else>
            <FormattedValue
              :value="row[h]"
              :format-config="{ dataType: 'currency-million' }"
            />
          </template>
        </td>
      </tr>
    </tbody>
  </v-table>
</template>

<script setup lang="ts">
import { computed } from "vue"
import FormattedValue from "@/components/FormattedValue.vue"
import { getObjectKeys } from "@/util"

const props = defineProps<{
  formulier: Record<string, any>
  hiddenFields: string[]
}>()

type RowLabel =
  | "Totaal"
  | "Intern personeel"
  | "Extern personeel"
  | "Overig materieel"

type RowData = {
  Kosten: RowLabel
  Actueel: number
  Daadwerkelijk: number
}

const tableData = computed((): RowData[] => {
  const rawData: RowData[] = [
    {
      Kosten: "Intern personeel",
      Actueel: parseFloat(
        props.formulier["Actueel intern personeel (correct)"],
      ),
      Daadwerkelijk: parseFloat(
        props.formulier["Daadwerkelijk intern personeel (correct)"],
      ),
    },
    {
      Kosten: "Extern personeel",
      Actueel: parseFloat(
        props.formulier["Actueel extern personeel (correct)"],
      ),
      Daadwerkelijk: parseFloat(
        props.formulier["Daadwerkelijk extern personeel (correct)"],
      ),
    },
    {
      Kosten: "Overig materieel",
      Actueel: parseFloat(
        props.formulier["Actueel overig materieel (correct)"],
      ),
      Daadwerkelijk: parseFloat(
        props.formulier["Daadwerkelijk overig materieel (correct)"],
      ),
    },
  ]
  const total = rawData.reduce(
    (totalRow: RowData, rowData) => {
      totalRow.Actueel = rowData.Actueel + totalRow.Actueel
      totalRow.Daadwerkelijk = rowData.Daadwerkelijk + totalRow.Daadwerkelijk
      return totalRow
    },
    {
      Kosten: "Totaal",
      Actueel: 0,
      Daadwerkelijk: 0,
    },
  )
  return [...rawData, total]
})

const tableHeaders = computed(() =>
  tableData.value.length > 0 ? getObjectKeys(tableData.value[0]) : [],
)
</script>

<style lang="scss" scoped>
@import "@/styles/_variables.scss";

table tr td,
th {
  padding: 5px 5px;
  text-align: left;
  font-size: $table-font-size;
  font-size: 0.59em !important;
}

table {
  margin-left: auto;
  margin-right: auto;
}

td.cell-total {
  font-weight: bold;
  font-family: "RO Sans Bold", sans-serif !important;
}

.v-table:deep(table) {
  width: auto !important;
}

.v-table:deep(.v-table__wrapper > table > tbody > tr > td) {
  font-size: 0.9em !important;
  padding: 0.4em 0.25em;
  height: auto !important;
}

.v-table:deep(.v-table__wrapper > table > tbody > tr > th) {
  font-size: 0.9em !important;
  padding: 0.5em 0.25em;
  height: auto !important;
}

.v-table {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
