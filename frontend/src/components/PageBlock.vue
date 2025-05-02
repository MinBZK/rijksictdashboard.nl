<template>
  <RidCol
    :key="title"
    :title="title"
    :fill-height="true"
    :img="imgUrl"
    :img-max-height="210"
    :title-in-bar="true"
    :img-copyright-text="imgAuthor ? ` Beeld: ${imgAuthor}` : ''"
    title-level="h3"
    class="rid-col"
  >
    <div :class="['snippet-text', mainPage ? 'mb-1' : 'mb-7']">
      <div v-html="description" />
      <div v-if="mainPage" class="mt-3">
        <v-icon>mdi-chevron-right</v-icon>

        <router-link :to="{ name: mainPage?.routeName }">
          {{ mainPage.title }}</router-link
        >
      </div>
    </div>

    <div class="py-2" :class="alignLinksToBottom && 'snippet-bottom'">
      <h3 v-if="mainPage">Meer informatie</h3>
      <v-row>
        <v-col v-for="(linksInColumn, index) in linksInColumns" :key="index">
          <div v-for="link in linksInColumn" :key="link.routeName">
            <v-icon>mdi-chevron-right</v-icon>
            <router-link
              :to="{
                name: link.routeName,
                query: {
                  from: route.name?.toString(),
                },
              }"
            >
              {{ link.label }}</router-link
            >
          </div>
        </v-col>
      </v-row>
    </div>
  </RidCol>
</template>

<script setup lang="ts">
import type { RidPage } from "@/content/pages"
import RidCol from "@/components/RidCol.vue"

type BlockLink = {
  routeName: string
  label: string
}

const props = withDefaults(
  defineProps<{
    title: string
    description?: string
    imgUrl: string
    imgAuthor?: string
    links: BlockLink[]
    alignLinksToBottom?: boolean
    mainPage?: RidPage
  }>(),
  {
    alignLinksToBottom: true,
  },
)

function transformArray<T>(inputArray: T[], subarrayLength: number): T[][] {
  return inputArray.reduce(
    (result: T[][], currentElement: T, index: number) => {
      const subarrayIndex = Math.floor(index / subarrayLength)

      if (!result[subarrayIndex]) {
        result[subarrayIndex] = []
      }

      result[subarrayIndex].push(currentElement)

      return result
    },
    [],
  )
}

const linksInColumns = computed((): BlockLink[][] => {
  const nColumns = props.links.length > 4 ? 2 : 1
  const linksPerColumn = Math.ceil(props.links.length / nColumns)
  return transformArray(props.links, linksPerColumn)
})

const route = useRoute()
</script>

<style scoped lang="scss">
@import "@/styles/main.scss";

.snippet-text {
  word-break: break-word;
  font-size: 0.9em;
  line-height: 1.5em;
}

.to-page {
  color: $hemelblauw;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.snippet-bottom {
  position: absolute;
  bottom: 0;
}

h3 {
  font-size: 0.95em;
}

.snippet-text a {
  font-size: 1.1rem;
}
</style>
