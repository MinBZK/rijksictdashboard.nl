<template>
  <page title="Onderwerpen">
    <div
      class="mb-5 description"
      v-html="getContent('Onderwerpen', 'content').value"
    />
    <RidRow title="Alle onderwerpen">
      <RidCol
        v-for="onderwerp in onderwerpen"
        :key="onderwerp"
        :fill-height="true"
        :has-border="true"
        :sm="6"
        :lg="4"
        :img="
          getOnderwerpContent(onderwerp)?.img
            ? `/img/onderwerpen/thumbnail/${
                getOnderwerpContent(onderwerp)?.img
              }`
            : '/img/placeholder-image.png'
        "
        :img-title="getTitle(onderwerp)"
        :img-copyright-text="
          getOnderwerpContent(onderwerp).imgAuthor
            ? `Beeld: ${getOnderwerpContent(onderwerp).imgAuthor}`
            : undefined
        "
        :route="{ name: 'onderwerp', params: { attributeValue: onderwerp } }"
      >
        {{ onderwerp }}
      </RidCol>
    </RidRow>
  </page>
</template>

<script setup lang="ts">
import type { Onderwerpen, Onderwerp } from "@/types/content"
import Page from "@/components/Page.vue"
import { getAggregation } from "@/services/project"

import { useContent } from "@/composables/useContent"
import RidRow from "@/components/RidRow.vue"
import RidCol from "@/components/RidCol.vue"
import { useTextLoader } from "@/composables/useTextLoader"

const { getContent } = useTextLoader()

const { content } = useContent()

let onderwerpenAgg = ref<Record<string, number> | null>(null)

const getData = async () => {
  onderwerpenAgg.value = await getAggregation({ attribute: "Onderwerp" })
}

const onderwerpen = computed(() =>
  onderwerpenAgg.value
    ? Object.keys(onderwerpenAgg.value)
        .filter((o) => o.length > 0)
        .sort()
    : [],
)

const getOnderwerpContent = (onderwerp: string): Onderwerp =>
  //@ts-expect-error
  content.onderwerp[(onderwerp as keyof Onderwerpen).trim()] as Onderwerp

getData()

const getTitle = (onderwerp: string) => {
  const content = getOnderwerpContent(onderwerp)
  return content.imgAuthor
    ? ` Beeld: ${getOnderwerpContent(onderwerp)?.imgAuthor}`
    : ""
}
</script>

<style scoped>
.page-desription-text {
  background-color: rgb(248, 248, 248);
}

.v-card:deep(.v-card-title) {
  white-space: normal !important;
  font-size: 1em;
}

div.img-wrapper {
  width: 100%;
  height: 230px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
div.img-wrapper img {
  height: 400px;
  width: 400px;
  object-fit: cover;
}

.description {
  max-width: 800px;
}
</style>
