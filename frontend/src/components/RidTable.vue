<template>
  <div>
    <v-table class="rid-table">
      <thead>
        <tr>
          <th
            v-for="header in headers"
            :key="header"
            class="no-wrap"
            scope="column"
          >
            {{
              typeof header == "string"
                ? capitalizeFirstLetter(getHeaderLabel(header))
                : getHeaderLabel(header)
            }}
            <span
              role="button"
              tabindex="0"
              :aria-label="getSortingStatus(header).aria"
              :title="getSortingStatus(header).aria"
              class="icon-button"
              :class="{
                'has-sorting': sortKey?.header == header,
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
        <tr v-for="(row, index) in paginatedData" :key="index">
          <td
            v-for="h in headers"
            :key="h"
            :class="{
              'text-right':
                getDataType(h) == 'currency-million' ||
                getDataType(h) == 'currency' ||
                getDataType(h) == 'number',
            }"
          >
            <template v-if="getColumnConfig(h)?.formatInSlot">
              <slot name="custom-table-cell" :cell-data="row" /> </template
            ><template v-else>
              <template v-if="getColumnConfig(h)?.link">
                <a
                  :href="row[h].toString() || '#'"
                  target="_blank"
                  rel="noopener"
                  >{{ getColumnConfig(h)?.link?.label || row[h] }}
                  {{ getLinkVariable(h, row) }}</a
                ></template
              >
              <template v-else>
                <FormattedValue
                  :value="row[h]"
                  :format-config="{ dataType: getDataType(h) || 'string' }"
                >
                  {{ row[h] }}
                </FormattedValue>
              </template>
            </template>
          </td>
        </tr>
      </tbody>
    </v-table>
    <Pagination
      v-if="tableData.length > rowsPerPage"
      v-model:page="page"
      title="ICT-activiteit"
      :total-count="tableData.length"
      :page-length="rowsPerPage"
      class="flex justify-space-between"
    />
  </div>
</template>

<script setup lang="ts" generic="T extends Record<string, any>">
import { sortArrayByKey } from "@/util"
import { capitalizeFirstLetter } from "@/util"
import FormattedValue from "@/components/FormattedValue.vue"
import type { TableConfig } from "@/types/table"

type SortKey = {
  header: keyof T
  ascending: boolean
}

const props = withDefaults(
  defineProps<{
    tableData: T[]
    columns: TableConfig<T>[]
    defaultSorting?: SortKey
    columnSequence?: (keyof T)[]
    rowsPerPage?: number
  }>(),
  {
    rowsPerPage: 20,
  },
)

const applyPagination = computed(
  () =>
    props.rowsPerPage != undefined &&
    props.rowsPerPage <= props.tableData.length,
)

const page = ref<number>(1)

const headers = computed(() => {
  const hiddenColumns = props.columns.filter((c) => c.hidden).map((c) => c.key)

  const allHeaders = [
    ...new Set(props.tableData.map((row) => Object.keys(row)).flat()),
  ]

  return (
    props.columnSequence ||
    allHeaders.filter((header) => !hiddenColumns.includes(header))
  )
})

const defaultSorting = toRef(props, "defaultSorting")
const sortKey = ref<SortKey | undefined>()
watch(
  defaultSorting,
  () => {
    sortKey.value = defaultSorting.value
  },
  { immediate: true },
)

const toggleSortKey = (header: keyof T) => {
  if (
    sortKey.value?.header == header &&
    !sortKey.value?.ascending &&
    props.defaultSorting?.header !== header
  ) {
    sortKey.value = props.defaultSorting
  } else if (sortKey.value?.header == header && sortKey.value?.ascending) {
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

const getSortingStatus = (header: keyof T) => {
  const headerString = typeof header == "string" ? header : header.toString()

  if (sortKey.value?.ascending === false && sortKey.value.header == header) {
    return {
      icon: "mdi-menu-down",
      aria: `Verwijder sortering voor ${headerString}`,
    }
  } else if (
    sortKey.value?.ascending === true &&
    sortKey.value.header == header
  ) {
    return {
      icon: "mdi-menu-up",
      aria: `Sorteer ${headerString} aflopend`,
    }
  } else {
    return {
      icon: "mdi-menu-swap",
      aria: `Sorteer ${headerString} oplopend`,
    }
  }
}

const sortedTableData = computed(() => {
  let sortedTableData = props.tableData
  const sortKeyHeader = sortKey.value?.header
  if (sortKeyHeader)
    sortedTableData = sortArrayByKey(sortedTableData, sortKeyHeader as keyof T)
  if (sortKey.value && !sortKey.value?.ascending)
    sortedTableData = sortedTableData.reverse()
  return sortedTableData
})

const paginatedData = computed(() => {
  if (!applyPagination.value) {
    return sortedTableData.value
  } else {
    const rowsPerPage = props.rowsPerPage
    if (!rowsPerPage) throw new Error("rowsPerPage is not defined")
    return sortedTableData.value.slice(
      (page.value - 1) * rowsPerPage,
      page.value * rowsPerPage,
    )
  }
})

function getColumnConfig(header: keyof T) {
  return props.columns.find((c) => c.key == header)
}

const getLinkVariable = (header: keyof T, row: T) => {
  const columnConfig = getColumnConfig(header)
  const columnVar = columnConfig?.link?.variableColumn

  return columnVar ? row[columnVar] : ""
}

function getDataType(header: keyof T) {
  const column = props.columns.find((c) => c.key == header)
  return column?.dataType
}

function getHeaderLabel(header: keyof T) {
  return getColumnConfig(header)?.label || header.toString()
}
</script>

<style scoped lang="scss">
@import "@/styles/_colors.scss";

.icon-button {
  color: $grijs6;
  font-size: 1em;
}

.icon-button:hover {
  color: $hemelblauw;
}

.rid-table > .v-table__wrapper > table > tbody > tr > th,
.rid-table > .v-table__wrapper > table > tbody > tr > td,
.rid-table > .v-table__wrapper > table > thead > tr > th,
.rid-table > .v-table__wrapper > table > tfoot > tr > th {
  font-size: 0.9em !important;
}

.rid-table > .v-table__wrapper > table > thead > tr > th {
  padding: 0 8px;
}

.rid-table > .v-table__wrapper > table > tbody > tr > td {
  padding: 8px 8px;
}

.icon-button.has-sorting {
  color: $hemelblauw;
}

.no-wrap {
  white-space: nowrap;
}

.v-table .v-table__wrapper > table > thead > tr > th {
  color: black;
}
</style>
