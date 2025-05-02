<template>
  <div v-if="crumbs && crumbs.length > 1" id="bc" class="breadcrumb-wrapper">
    <div class="breadcrumb-wrapper-content">
      <v-row class="mx-2 my-1">
        <v-col cols="12" :md="7" :lg="8">
          <nav>
            <span
              v-for="({ label, targetRoute }, index) in crumbs"
              :key="label"
              class="crumb"
            >
              <router-link
                v-if="index + 1 !== crumbs.length"
                :to="targetRoute"
                >{{ label }}</router-link
              >
              <span v-if="index + 1 == crumbs.length">{{ label }}</span>
              <v-icon v-if="index + 1 < crumbs.length"
                >mdi-chevron-right</v-icon
              >
            </span>
          </nav>
        </v-col>
        <v-col cols="12" :md="5" :lg="4" class="py-0">
          <SearchBar :apply-collapsing="true" />
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from "vue-router"
import type {
  RouteRecordRaw,
  RouteLocationNormalizedLoaded,
  RouteParams,
} from "vue-router"
import { useGlobalStore } from "@/store/useGlobalStore"
import { capitalizeFirstLetter } from "@/util"
import SearchBar from "@/views/SearchBar.vue"
import { useRouteQuery } from "@vueuse/router"
import type { ParentRouteQuery } from "@/types/router"

const { state } = useGlobalStore()

const currentRoute = useRoute()
const router = useRouter()

type RouterLink = {
  name: string
  params?: Record<string, string>
}

type Crumb = {
  label: string
  parent?: Crumb
  targetRoute: RouterLink
}

// Route param values are of type string | string[], but we don't use arrays in this case.
const getFirstValueFromArray = (v: string | string[]) =>
  Array.isArray(v) ? v[0] : v

const labels = computed((): Record<string, string | undefined> => {
  return {
    // Check if current project is loading to prevent displaying project name from previous visited page.
    "ict-activiteit": state.loadingCurrentProject
      ? ""
      : state.currentProject?.Naam,
    onderwerp: getFirstValueFromArray(currentRoute.params["attributeValue"]),
    ministerie: getFirstValueFromArray(currentRoute.params["attributeValue"]),
    "wat we verbeteren detail": "Wat we verbeteren",
    soort: "Soort ICT-activiteit",
  }
})

function getCrumbLabelFromRoute(
  route: RouteLocationNormalizedLoaded | RouteRecordRaw,
) {
  const routeName = route.name?.toString()
  // Returns the label for the crumb based on the route. This is shown to the user.
  if (!routeName) throw Error(`No route name defined ${routeName}`)
  const customLabel = labels.value[routeName]
  const routeLabel =
    customLabel !== undefined
      ? customLabel
      : capitalizeFirstLetter(route.meta?.label || routeName)
  return getLabelFromQueryOverride(routeName) || routeLabel || ""
}

// Returns the label for the route if an override is specified in the URL via query parameters.
// This will be displayed in the breadcrumb.
const getLabelFromQueryOverride = (routeName: string) =>
  parentRouteOverride.value?.from == routeName &&
  parentRouteOverride.value.label
    ? getFirstValueFromArray(parentRouteOverride.value.label)
    : undefined

function getRouteParams(
  routeParams: RouteParams | undefined,
  routeName: string,
) {
  // Returns the route params that are used in the router link.
  const routeIdMapping: Record<string, string> = {
    "ict-activiteit": "projectId",
  }

  if (routeParams && routeName) {
    return {
      key: routeIdMapping[routeName] || Object.keys(routeParams)[0],
      value: routeParams[Object.keys(routeParams)[0]],
    }
  }
}

function getParentRoute(routeName: string | undefined) {
  // Returns the parent route based on the route name.
  const allParentRoutes = router.options.routes
  const allChildRoutes = allParentRoutes.flatMap((r) => r.children || [])
  const allRoutes = allParentRoutes.concat(allChildRoutes)
  return allRoutes.find((r) => r.name == routeName)
}

const getCrumbs = (
  route: RouteLocationNormalizedLoaded | RouteRecordRaw,
  allCrumbs: Crumb[],
  routeParams: RouteParams | undefined,
  parentRouteOverride: ParentRouteQuery | undefined,
): Crumb[] | undefined => {
  // Recursively get a list of routes by determining the parent route of the current route.
  // Ends when no parent route is found.
  const routeName = route.name?.toString()
  const parentRouteName =
    parentRouteOverride?.from || route.meta?.parentRouteName
  const parentRoute = getParentRoute(parentRouteName)

  if (route && routeName) {
    const label = getCrumbLabelFromRoute(route)
    const params = getRouteParams(routeParams, routeName)

    const targetRoute: RouterLink = {
      name: routeName,
      params: params
        ? {
            [params.key]: getFirstValueFromArray(params.value),
          }
        : undefined,
    }

    allCrumbs.push({
      label,
      targetRoute,
    })
    if (parentRoute && parentRouteName !== "catchAll") {
      const parentRouteParams = parentRouteOverride?.id
        ? { id: parentRouteOverride.id }
        : undefined

      return getCrumbs(parentRoute, allCrumbs, parentRouteParams, undefined)
    } else {
      return allCrumbs
    }
  } else {
    return allCrumbs
  }
}
const crumbs = computed(() =>
  getCrumbs(
    currentRoute,
    [],
    currentRoute.params,
    parentRouteOverride.value,
  )?.reverse(),
)

// Pages can have multiple entry paths, therefore the parent route can vary.
// The parent route can be specified in the URL via query parameters.
const parentRouteNameOverride = useRouteQuery("from")
const parentRouteParamOverride = useRouteQuery("id")
const parentRouteLabelOverride = useRouteQuery("label")

const parentRouteOverride = computed((): ParentRouteQuery | undefined => {
  return parentRouteNameOverride.value
    ? {
        from: getFirstValueFromArray(parentRouteNameOverride.value),
        id: parentRouteParamOverride.value
          ? getFirstValueFromArray(parentRouteParamOverride.value)
          : undefined,
        label: parentRouteLabelOverride.value
          ? getFirstValueFromArray(parentRouteLabelOverride.value)
          : undefined,
      }
    : undefined
})
</script>

<style scoped lang="scss">
@import "@/styles/main.scss";

a {
  color: $headerTextColour;
}

a:hover {
  color: unset !important;
}
.breadcrumb-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: $secondary;
  min-height: 56px;
}

.breadcrumb-wrapper-content {
  max-width: 1200px;
  display: flex;
  width: 100%;
  justify-content: space-between;
  font-size: 19px;
  color: $headerTextColour;
}

.crumb-label {
  margin-right: 0.75em;
}
</style>
