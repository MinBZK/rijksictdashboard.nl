<template>
  <page title="Ministeries">
    <div
      class="mb-5 description"
      v-html="getContent('Ministeries', 'content').value"
    />

    <RidRow title="Alle ministeries">
      <RidCol
        v-for="{ Naam: ministerie } in ministeries"
        :key="ministerie"
        :fill-height="true"
        :sm="6"
        :has-border="true"
        :lg="4"
        :img="
          getMinisterieContent(ministerie)?.img
            ? `/img/ministeries/thumbnail/${
                getMinisterieContent(ministerie)?.img
              }`
            : '/img/placeholder-image.png'
        "
        :img-title="getImgTitle(ministerie)"
        :img-copyright-text="
          getMinisterieContent(ministerie).imgAuthor
            ? `Beeld: ${getMinisterieContent(ministerie).imgAuthor}`
            : undefined
        "
        :route="{
          name: 'ministerie',
          params: { attributeValue: ministerie },
        }"
      >
        Ministerie van {{ ministerie }}
      </RidCol>
    </RidRow>
  </page>
</template>

<script setup lang="ts">
import Page from "@/components/Page.vue"
import { useContent } from "@/composables/useContent"
import type { Ministerie, Ministeries } from "@/types/content"
import RidRow from "@/components/RidRow.vue"
import RidCol from "@/components/RidCol.vue"
import { useMinisterie } from "@/composables/useMinisterie"
import { useTextLoader } from "@/composables/useTextLoader"

const { getContent } = useTextLoader()

const { content } = useContent()
const { ministeries } = useMinisterie()

const getMinisterieContent = (ministerie: string): Ministerie =>
  content.ministerie[
    (ministerie || "").trim() as keyof Ministeries
  ] as Ministerie

const getImgTitle = (ministerie: string) => {
  const content = getMinisterieContent(ministerie)
  return content.imgAuthor
    ? ` Beeld: ${getMinisterieContent(ministerie)?.imgAuthor}`
    : ""
}
</script>

<style scoped>
.v-card:deep(.v-card-title) {
  /* white-space: normal !important; */
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
</style>
