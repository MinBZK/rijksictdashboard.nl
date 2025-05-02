<template>
  <Page title="Sitemap" :text-only="true">
    <TextLoaderContent content-field-key="content" content-group="Sitemap" />
    <ul>
      <li
        v-for="(item, routeIndex) in nameAndPath.filter((r) => r.name)"
        :key="routeIndex"
      >
        <a :v-if="item.name" :href="item.fullPath"
          >{{ item && item.name ? capitalize(item.name as string) : "" }}
        </a>
        <template v-if="item.name === 'ministeries'"
          ><ul>
            <li
              v-for="(ministerie, ministerieIndex) in ministeries"
              :key="ministerieIndex"
            >
              <router-link
                :to="{
                  name: 'ministerie',
                  params: { attributeValue: ministerie.Naam },
                }"
                >{{ ministerie.Naam }}</router-link
              >
            </li>
          </ul></template
        >
        <template v-if="item.name === 'onderwerpen'"
          ><ul>
            <li v-for="(onderwerp, index) in onderwerpen" :key="index">
              <router-link
                :to="{
                  name: 'onderwerp',
                  params: { attributeValue: onderwerp },
                }"
                >{{ onderwerp }}</router-link
              >
            </li>
          </ul></template
        >
      </li>
    </ul>
  </Page>
</template>

<script setup lang="ts">
import Page from "@/components/Page.vue"
import { useRouter } from "vue-router"
import { useMinisterie } from "@/composables/useMinisterie"
import { useContent } from "@/composables/useContent"
import type { RouteRecordRaw } from "vue-router"
import TextLoaderContent from "@/components/TextLoaderContent.vue"

const router = useRouter()

const allRoutes = router.options.routes

const { content } = useContent()

const onderwerpen = Object.keys(content.onderwerp)

const { ministeries } = useMinisterie()

const excludePages = ["/pagina-niet-gevonden", "/sitemap"]

type CalculatedRoute = RouteRecordRaw & {
  fullPath: string
}

const nameAndPath = computed(() =>
  allRoutes
    .filter(({ path }) => !path.includes(":"))
    .filter(({ path }) => !excludePages.includes(path))
    .map((r) => {
      let route: CalculatedRoute = { ...r, fullPath: r.path }
      let childRootRoute = r.children?.find((r) => r.path == "")
      if (childRootRoute) {
        route = { ...childRootRoute, fullPath: r.path }
      }
      return route
    })
    .map(({ name, fullPath }) => ({ name, fullPath })),
)

const capitalize = (string: string) =>
  string.charAt(0).toUpperCase() + string.slice(1)
</script>

<style scoped lang="scss">
@import "@/styles/main.scss";
ul {
  padding-left: 20px;
}
</style>
