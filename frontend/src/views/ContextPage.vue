<template>
  <Page
    v-if="page && pageTitle"
    :title="page.title"
    :title-category="attributeValue"
    :description="previewText"
  >
    <p v-if="!hidePreview" class="mb-3 description">
      {{ previewText }}
    </p>

    <ExpandContent
      v-if="expandable"
      :key="page.title"
      :title="`Lees meer over ${page.title}`"
    >
      <router-view
    /></ExpandContent>

    <router-view v-if="!expandable" />

    <RidRow
      v-if="contextGroupName !== 'Overig' && otherPages.length > 0"
      :title="`Meer informatie over ${contextGroupName}`"
      title-level="h2"
    >
      <PageBlock
        v-for="p in otherPages"
        :key="p.routeName"
        :title="p.longTitle || p.title"
        :description="
          getContent(p.previewText.contentKey, p.previewText.contentName).value
        "
        :img-url="p.image.imgUrl"
        :img-author="p.image.imgAuthor"
        :sm="4"
        :lg="4"
        :links="[
          {
            routeName: p.routeName,
            label: p.title,
          },
        ]"
      />
    </RidRow>
  </Page>
</template>

<script setup lang="ts">
import { pages, pageGroups } from "@/content/pages"
import Page from "@/components/Page.vue"
import PageBlock from "@/components/PageBlock.vue"
import RidRow from "@/components/RidRow.vue"
import { useTextLoader } from "@/composables/useTextLoader"
import ExpandContent from "@/components/ExpandContent.vue"
import { sortArrayByKey } from "@/util"

withDefaults(
  defineProps<{
    expandable?: boolean
    hidePreview?: boolean
  }>(),
  {
    expandable: true,
    hidePreview: false,
  },
)

const route = useRoute()
const { getContent } = useTextLoader()

const allPages = [...pages, ...pageGroups.map((pG) => pG.mainPage)]

const page = computed(() =>
  allPages.find(
    (p) =>
      p.routeName == route.name ||
      (route.name && p.alternativeEntryRouteNames?.includes(route.name)),
  ),
)

const attributeValue = computed(() => {
  const val = route.params["attributeValue"]
  return Array.isArray(val) ? val[0] : val
})

const pageTitle = computed(() => {
  const pageTitle = page.value?.title
  if (attributeValue) {
    return `${pageTitle} - ${attributeValue}`
  } else {
    return pageTitle
  }
})

const contextGroupName = computed(() => {
  return page.value?.contextGroupName || page.value?.groupName
})

const otherPages = computed(() =>
  sortArrayByKey(
    allPages.filter(
      (p) =>
        p.groupName == contextGroupName.value &&
        p.routeName !== page.value?.routeName,
    ),
    "title",
  ),
)

const previewText = computed(() => {
  return page.value
    ? getContent(
        page.value.previewText.contentKey,
        page.value.previewText.contentName,
      ).value
    : undefined
})
</script>

<style scoped lang="scss">
.description {
  max-width: 800px;
}
</style>
