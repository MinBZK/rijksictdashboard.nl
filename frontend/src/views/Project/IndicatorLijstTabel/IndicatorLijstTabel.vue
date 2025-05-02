<template>
  <v-row v-if="tiles">
    <RijksoverheidCardField
      v-for="fW in getFormulierWaardes(sortedFormulieren[0])"
      :key="fW?.IndicatorTitel"
      :title="
        fW?.IndicatorTitel // @ts-expect-error
          ? indicatorTitelMapping[fW?.IndicatorTitel] || fW.IndicatorTitel
          : fW?.IndicatorTitel
      "
    >
      <IndicatorLijstTabelWaarde
        :indicator="fW"
        :scroll-on-click="fW ? getScroll(fW) : undefined"
      />
    </RijksoverheidCardField>
  </v-row>
  <v-table
    v-if="
      hasFormulier &&
      !props.tiles &&
      (indicatorLijst?.IndicatorLijstEnkelFormulier ||
        (indicatorLijst?.IndicatorLijstMeervoudsNaam
          ? cmsConfig.general.indicatorLijstEnkel.includes(
              indicatorLijst?.IndicatorLijstMeervoudsNaam,
            )
          : false))
    "
    class="indicator-table"
  >
    <colgroup>
      <col span="1" :class="mdAndUp ? 'title-col-lg' : 'title-col'" />
    </colgroup>
    <tbody>
      <tr v-for="h in headers" :key="h">
        <th class="v-align-top" scope="row">
          {{ h }}
        </th>
        <IndicatorLijstTabelCel
          :indicator="
            sortedFormulieren[0].FormulierWaardes.find(
              (fW) => fW.IndicatorTitel == h,
            )
          "
          :always-align-left="true"
        />
      </tr>
    </tbody>
  </v-table>
  <v-table v-else-if="!tiles && hasFormulier" class="indicator-table">
    <thead>
      <tr>
        <!-- dummy column for expand icon -->
        <th v-if="hiddenFields.length > 0" scope="column"></th>
        <th
          v-for="h in headers"
          :key="h"
          scope="column"
          class="cursor-pointer"
          @click="handleSortClick(h)"
        >
          <span class="title-with-indicator">
            {{ h }}
            <span
              v-if="
                sortKey === h && (sortOrder == 'asc' || sortOrder === 'desc')
              "
            >
              {{ sortOrder === "asc" ? "▲" : "▼" }}
            </span>
          </span>
        </th>
      </tr>
    </thead>
    <tbody>
      <IndicatorLijstTabelRij
        v-for="(formulier, index) in sortedFormulieren"
        :key="index"
        :headers="headers"
        :formulier="formulier"
        :url-fields="urlFields"
        :hidden-fields="hiddenFields"
      >
        <table
          v-if="
            indicatorLijst?.IndicatorLijstMeervoudsNaam !==
            'Doorlooptijd en Kosten'
          "
        >
          <caption>
            {{
              indicatorLijst?.IndicatorLijstMeervoudsNaam
            }}
          </caption>
          <thead>
            <tr>
              <th>Veld</th>
              <th>Waarde</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="h in hiddenFields" :key="h">
              <IndicatorLijstTabelCel
                :indicator="
                  formulier.FormulierWaardes.find(
                    (fW) => fW.IndicatorTitel == h,
                  )
                "
              />
            </tr>
          </tbody>
        </table>

        <IndicatorLijstDetailsDoorlooptijdEnKosten
          v-else-if="formulier && formulier.Dict"
          :formulier="formulier.Dict"
          :hidden-fields="hiddenFields"
        />
      </IndicatorLijstTabelRij>
    </tbody>
  </v-table>

  <span v-else-if="!hasFormulier">Geen informatie beschikbaar.</span>
</template>

<script setup lang="ts">
import type { Formulier, FormulierWaarde } from "@/api-new"
import type { IndicatorLijstMetBerekendeAttributen } from "@/types/indicatorlijst"
import IndicatorLijstTabelRij from "./IndicatorLijstTabelRij.vue"
import IndicatorLijstTabelWaarde from "./IndicatorLijstTabelWaarde.vue"
import type { ScrollOnClick } from "./IndicatorLijstTabelWaarde.vue"
import IndicatorLijstDetailsDoorlooptijdEnKosten from "./IndicatorLijstDetailsDoorlooptijdEnKosten.vue"
import { flattenArray, getUniqueValues, sortArrayByKey } from "@/util"
import { getFormulierAsDict } from "@/util/cms"
import cmsConfig from "@/config/cms"
import type { IndicatorLijstenConfig } from "@/config/cms"
import RijksoverheidCardField from "@/components/RidColField.vue"
import IndicatorLijstTabelCel from "./IndicatorLijstTabelCel.vue"
import { useDisplay } from "vuetify"

const { mdAndUp } = useDisplay()

const indicatorTitelMapping = {
  "Maatschappelijk baat": "Interne verbeteringen",
}

const props = withDefaults(
  defineProps<{
    formulieren?: Formulier[]
    tiles?: boolean
    indicatorLijst?: IndicatorLijstMetBerekendeAttributen
    indicatorTitelSequence?: string[]
    excludedIndicatoren?: string[]
    indicatorTitleDivId?: Record<string, ScrollOnClick>
  }>(),
  {
    tiles: false,
    excludedIndicatoren: () => [],
  },
)

const sortKey = ref<string | null>(null)
const sortOrder = ref<"asc" | "desc" | "neutral">("asc")

const sortOrderCycle: Record<
  "asc" | "desc" | "neutral",
  "asc" | "desc" | "neutral"
> = {
  asc: "desc",
  desc: "neutral",
  neutral: "asc",
}

function handleSortClick(key: string) {
  if (sortKey.value === key) {
    sortOrder.value = sortOrderCycle[sortOrder.value]
  } else {
    sortKey.value = key
    sortOrder.value = "asc"
  }
}

const indicatorLijstConfig = computed(() => {
  return cmsConfig.indicatorLijsten[
    props.indicatorLijst
      ?.IndicatorLijstMeervoudsNaam as keyof IndicatorLijstenConfig
  ]
})

const hiddenFields = computed(() =>
  indicatorLijstConfig.value
    ? indicatorLijstConfig.value.hiddenFields || []
    : [],
)

const urlFields = computed(() =>
  indicatorLijstConfig.value ? indicatorLijstConfig.value.urlFields || [] : [],
)

const sortedFormulieren = computed(() => {
  const result =
    props.formulieren || props.indicatorLijst?.FormulierGefilterd || []

  const sortableIndex = "sortableIndexValue"
  const sortableFormulieren = result.map((formulier) => {
    return {
      ...formulier,
      [sortableIndex]:
        sortKey.value && sortKey.value.length > 0
          ? formulier.FormulierWaardes?.find(
              (fW) => fW.IndicatorTitel === sortKey.value,
            )?.Waarde
          : formulier.FormulierAanmaakDatum,
    }
  })

  const sortedFormulieren = sortArrayByKey(
    sortableFormulieren,
    sortableIndex,
    sortOrder.value == "neutral" ? "asc" : sortOrder.value,
  )

  return sortedFormulieren
})

watch(sortOrder, (newSortOrder) => {
  if (newSortOrder === "neutral") {
    sortKey.value = null
  }
})

watch(sortOrder, (newSortOrder) => {
  if (newSortOrder === "neutral") {
    sortKey.value = null
  }
})

watch(sortOrder, (newSortOrder) => {
  if (newSortOrder === "neutral") {
    sortKey.value = null
  }
})

const formulierenDict = computed(() => {
  return sortedFormulieren.value.map((f) => getFormulierAsDict(f))
})

const hasFormulier = computed(() => formulierenDict.value.length > 0)

const headersSortedOnIndicatorIndex = computed(() => {
  const sortedArray = sortedFormulieren.value.map((f) => {
    return sortArrayByKey(
      f.FormulierWaardes.map((fW) => {
        return { key: fW.IndicatorTitel, index: fW.IndicatorIndex }
      }),
      "index",
    )
  })
  const flatArray = flattenArray(sortedArray).sort((a, b) => a.index - b.index)
  const uniqueHeaderArray = getUniqueValues(flatArray.map((v) => v["key"]))
  return uniqueHeaderArray.filter((h) => !hiddenFields.value.includes(h))
})

const headers = computed(() => {
  const customDefinedHeaders = props.indicatorTitelSequence || []

  const headersNotDefinedInSequence =
    headersSortedOnIndicatorIndex.value.filter(
      (h) => !customDefinedHeaders.includes(h),
    )

  const headersCustomDefinedWithoutMissingHeaders = customDefinedHeaders.filter(
    (h) => headersSortedOnIndicatorIndex.value.includes(h),
  )

  return [
    ...headersCustomDefinedWithoutMissingHeaders,
    ...headersNotDefinedInSequence,
  ].filter((h) => !props.excludedIndicatoren.includes(h))
})

const getScroll = (formulierWaarde: FormulierWaarde) => {
  return props.indicatorTitleDivId?.[formulierWaarde.IndicatorTitel]
}

const getFormulierWaardes = (formulier: Formulier) => {
  return headers.value
    .map((h) => {
      const fW = formulier.FormulierWaardes.find((fW) => fW.IndicatorTitel == h)
      return fW
    })
    .filter((fW) => fW?.Waarde)
}
</script>

<style lang="scss" scoped>
@import "@/styles/_colors.scss";
@import "@/styles/_variables.scss";

.title-col-lg {
  width: 300px;
}

.title-col {
  width: 150px;
}

td {
  vertical-align: top;
}

.indicator-table > .v-table__wrapper > table > tbody > tr > th,
.indicator-table > .v-table__wrapper > table > tbody > tr > td,
.indicator-table > .v-table__wrapper > table > thead > tr > th,
.indicator-table > .v-table__wrapper > table > tfoot > tr > th {
  font-size: $table-font-size !important;
}

// .indicator-table:deep(.v-table__wrapper) {
//   overflow: visible !important;
// }

.box {
  display: flex;
  align-items: center;
  justify-content: center;
}

.box div {
  width: 100px;
  height: 100px;
}

.v-table .v-table__wrapper > table > thead > tr > th {
  color: black;
}

.v-align-top {
  vertical-align: top;
}

.cursor-pointer {
  cursor: pointer;
}

.title-with-indicator {
  display: inline-flex;
  align-items: center;
}
</style>
