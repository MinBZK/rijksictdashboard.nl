<template>
  <v-table v-if="sortedTableData.length > 0" class="rid-tabel">
    <caption class="mb-3 mt-5 font-italic text-right">
      Cijfers zijn in miljoenen euro's
    </caption>
    <thead>
      <tr>
        <td colspan="1"></td>
        <th
          v-for="h in categoryValues['categorie']"
          :key="h"
          scope="column"
          :colspan="categoryValues['kostenpost'].length"
        >
          {{ capitalizeFirstLetter(h.toString()) }}
        </th>
      </tr>
      <tr>
        <th
          v-for="header in headers"
          :key="header"
          scope="column"
          class="no-wrap"
        >
          {{
            capitalizeFirstLetter(
              header.split("_").length > 1 ? header.split("_")[0] : header,
            )
          }}
          <span
            role="button"
            tabindex="0"
            :aria-label="getSortingStatus(header).aria"
            :title="getSortingStatus(header).aria"
            class="icon-button"
            :class="{
              'has-sorting': sortKey.header == header,
            }"
            @click="toggleSortKey(header)"
            @keydown.space="toggleSortKey(header)"
            @keydown.enter="toggleSortKey(header)"
            ><v-icon :icon="getSortingStatus(header).icon"
          /></span>
        </th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(row, index) in sortedTableData" :key="index">
        <td
          v-for="header in headers"
          :key="header"
          :class="header != 'ministerie' && 'text-right'"
        >
          <FormattedValue
            v-if="header != 'ministerie'"
            :value="row[header]"
            :format-config="{
              dataType: 'number',
              minimumDigits: 2,
              maximumDigits: 2,
            }"
          />
          <template v-if="header == 'ministerie'">{{ row[header] }}</template>
        </td>
      </tr>
    </tbody>
  </v-table>
</template>

<script setup lang="ts">
import type { IctKostenDataPoint } from "@/types/ictkosten"
import FormattedValue from "@/components/FormattedValue.vue"
import { sortArrayByKey } from "@/util"
import { capitalizeFirstLetter } from "@/util"

const props = defineProps<{
  tableData: IctKostenDataPoint[]
}>()

const headers = [
  "ministerie",
  "intern personeel_beheer en onderhoud",
  "extern personeel_beheer en onderhoud",
  "overig materieel_beheer en onderhoud",
  "intern personeel_vernieuwing",
  "extern personeel_vernieuwing",
  "overig materieel_vernieuwing",
]

const sortedTableData = computed(() => {
  const ministeries = categoryValues.value.ministerie
  const kostenposten = categoryValues.value.kostenpost
  const categorieen = categoryValues.value.categorie

  const tableData = ministeries.map((m) => {
    const row: { [key: string]: string | number | undefined } = {
      ministerie: m,
    }
    kostenposten.forEach((k) =>
      categorieen.forEach((c) => {
        const columnKey = k.toString() + "_" + c.toString()
        row[columnKey] = props.tableData.find(
          (cell) =>
            cell.categorie == c && cell.kostenpost == k && cell.ministerie == m,
        )?.kosten
      }),
    )
    return row
  })
  const sortedData = sortArrayByKey(tableData, sortKey.value.header)
  if (!sortKey.value.ascending) {
    return sortedData.reverse()
  } else {
    return sortedData
  }
})

const categoryValues = computed(() =>
  (
    ["categorie", "kostenpost", "ministerie"] as (keyof IctKostenDataPoint)[]
  ).reduce(
    (obj, property) => {
      obj[property] = [...new Set(props.tableData.map((row) => row[property]))]
      return obj
    },
    {} as Record<keyof IctKostenDataPoint, (string | number)[]>,
  ),
)

type SortKey = {
  header: string
  ascending: boolean
}

const defaultSorting: SortKey = { header: "ministerie", ascending: true }
const sortKey = ref<SortKey>(defaultSorting)

const toggleSortKey = (header: string) => {
  if (sortKey.value.header == header && !sortKey.value.ascending) {
    sortKey.value = defaultSorting
  } else if (sortKey.value.header == header && sortKey.value.ascending) {
    sortKey.value = {
      header,
      ascending: false,
    }
  } else {
    sortKey.value = {
      header,
      ascending: true,
    }
  }
}

const getSortingStatus = (header: string) => {
  if (sortKey.value?.ascending === false && sortKey.value.header == header) {
    return {
      icon: "mdi-menu-down",
      aria: `Verwijder sortering voor ${header}`,
    }
  } else if (
    sortKey.value?.ascending === true &&
    sortKey.value.header == header
  ) {
    return {
      icon: "mdi-menu-up",
      aria: `Sorteer ${header} aflopend`,
    }
  } else {
    return {
      icon: "mdi-menu-swap",
      aria: `Sorteer ${header} oplopend`,
    }
  }
}
</script>

<style scoped lang="scss">
@import "@/styles/_colors.scss";

.no-wrap {
  white-space: nowrap;
}
.icon-button {
  color: $grijs6;
  font-size: 1em;
}

.icon-button:hover {
  color: $hemelblauw;
}

.rid-tabel > .v-table__wrapper > table > tbody > tr > th,
.rid-tabel > .v-table__wrapper > table > tbody > tr > td,
.rid-tabel > .v-table__wrapper > table > thead > tr > th,
.rid-tabel > .v-table__wrapper > table > tfoot > tr > th {
  font-size: 0.9em !important;
}

.rid-tabel > .v-table__wrapper > table > thead > tr > th {
  padding: 0 8px;
}

.rid-tabel > .v-table__wrapper > table > tbody > tr > td {
  padding: 8px 8px;
}

.icon-button.has-sorting {
  color: $hemelblauw;
}

caption {
  caption-side: bottom;
}
</style>
