<template>
  <template
    v-if="
      !valueIsUrl &&
      indicator?.IndicatorAntwoordTypeNaam !== 'MeerKeuze' &&
      splittedValues.length == 1
    "
  >
    <FormattedValue
      v-if="
        indicator?.IndicatorAntwoordTypeNaam !==
        ('MeerKeuze' as IndicatorAntwoordTypeNaam)
      "
      :value="indicator?.Waarde"
      :format-config="{ dataType }"
      :value-title="indicator?.IndicatorTitel"
      :route="getRoute(indicator?.IndicatorTitel, indicator?.Waarde)"
      :scroll-div-id="targetDivId"
    />
  </template>
  <template
    v-else-if="
      !valueIsUrl &&
      splittedValues.length > 1 &&
      indicator?.IndicatorAntwoordTypeNaam == 'MeerKeuze'
    "
  >
    <div>
      <ul>
        <li v-for="splittedValue in splittedValues" :key="splittedValue">
          <FormattedValue
            :value="splittedValue"
            :format-config="{ dataType }"
            :value-title="indicator?.IndicatorTitel"
            :route="getRoute(indicator?.IndicatorTitel, splittedValue)"
          />
        </li>
      </ul>
    </div>
  </template>
  <template
    v-else-if="
      !valueIsUrl || (indicator?.Waarde && !isValidUrl(indicator?.Waarde))
    "
  >
    <FormattedValue
      :value="indicator?.Waarde"
      :format-config="{ dataType }"
      :value-title="indicator?.IndicatorTitel"
      :route="getRoute(indicator?.IndicatorTitel, indicator?.Waarde)"
    />
  </template>

  <template v-else-if="indicator?.Waarde">
    <a :href="indicator.Waarde" target="_blank" class="btn-link no-icon">
      <RidButton type="submit" prepend-icon="mdi-file"
        >Bekijk document</RidButton
      >
    </a>
  </template>
</template>

<script setup lang="ts">
import FormattedValue from "@/components/FormattedValue.vue"
import type { RouteLocationRaw } from "vue-router"
import { isValidUrl } from "@/util"
import RidButton from "@/components/RidButton.vue"
import cmsConfig from "@/config/cms"
import type { ParentRouteQuery } from "@/types/router"
import { useGlobalStore } from "@/store/useGlobalStore"

import type {
  // IndicatorWaarde,
  IndicatorAntwoordTypeNaam,
} from "@/types/indicatorlijst"

import type { FormulierWaarde } from "@/api-new"
import type { ProjectAttribute } from "@/types/project"

export type ScrollOnClick = {
  divId: string
  value?: "Ja"
}

const props = withDefaults(
  defineProps<{
    indicator?: FormulierWaarde
    valueIsUrl?: boolean
    scrollOnClick?: ScrollOnClick
  }>(),
  {
    valueIsUrl: false,
  },
)

const dataType = computed(() => {
  const indicatorAntwoordMapping = {
    Bedrag: "currency",
    Datum: "date",
    Getal: "number",
    Tabelcel: "currency",
  }

  return props.indicator?.IndicatorAntwoordTypeNaam
    ? //@ts-expect-error
      indicatorAntwoordMapping[props.indicator.IndicatorAntwoordTypeNaam] ||
        undefined
    : undefined
})

const splittedValues = computed(() => props.indicator?.Waarde?.split(";") || [])

const route = useRoute()
const { state } = useGlobalStore()

const getFirstValueFromArray = (v: string | string[]) => {
  // route param value are of type string | string[]
  if (Array.isArray(v)) {
    return v[0]
  } else {
    return v
  }
}

const getRoute = (
  indicatorTitel: string | undefined,
  waarde: string | undefined | null,
) => {
  const projectAttributeDict: Record<string, ProjectAttribute> = {
    Ministerie: "MinisterieNaam",
    Onderwerp: "Onderwerp",
    "Soort ICT-activiteit": "SoortICTActiviteit",
    "Maatschappelijk baat": "MaatschappelijkeBaat",
    "Samenwerkende ministerie(s)": "MinisterieNaam",
  }

  const attributesWithLink: ProjectAttribute[] =
    Object.values(projectAttributeDict)

  const projectAttribute = indicatorTitel
    ? projectAttributeDict[indicatorTitel]
    : undefined

  if (
    projectAttribute &&
    waarde &&
    attributesWithLink.includes(projectAttribute)
  ) {
    const routerName = cmsConfig.attributeConfig[projectAttribute]?.routerName

    const routeQuery: ParentRouteQuery | undefined = route.name
      ? {
          from: route.name?.toString(),
          id: getFirstValueFromArray(route.params.projectId),
          label: state.currentProject?.Naam,
        }
      : undefined

    const composedRoute: RouteLocationRaw = {
      name: routerName,
      params: { attributeValue: waarde },
      query: routeQuery,
    }

    return composedRoute
  } else {
    return undefined
  }
}

const targetDivId = computed(() =>
  props.scrollOnClick && props.indicator?.Waarde == props.scrollOnClick.value
    ? props.scrollOnClick.divId
    : undefined,
)
</script>

<style scoped lang="scss">
.v-chip {
  margin: 3px 1px;
}

a.btn-link:hover {
  text-decoration: none !important;
}

ul {
  padding-left: 1em;
}
</style>
