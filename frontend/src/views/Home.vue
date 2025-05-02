<template>
  <Page title="" :scroll-to-content="false">
    <template #page-before>
      <div class="home-image">
        <div style="max-width: 1200px; margin: 0 auto">
          <v-row no-gutters class="py-15 px-3">
            <v-col id="content" cols="12" class="home-image-text mb-4" :lg="6">
              <v-sheet class="pa-2 ma-2">
                <h1 class="text-h5">
                  Informatie over digitalisering van de Rijksoverheid
                </h1>
                <!-- <span v-html="getContent('Home', 'Introductie').value" /> -->
                <TextLoaderContent
                  content-group="Home"
                  content-field-key="Introductie"
                  class="no-bottom-margin"
                />
              </v-sheet>
            </v-col>
            <v-col cols="0" :lg="2"></v-col>
            <v-col cols="12" :lg="4"> <SearchBar /></v-col>
          </v-row>
        </div>
      </div>
    </template>
    <Metrics
      :filters="[]"
      :hidden-charts="['Doorlooptijd (aantallen)']"
      :show-ict-kosten="false"
      :auto-load="true"
      :show-full-title="true"
      title-level="h2"
      :introduction-text-with-link="true"
      :is-home-page="true"
    />
    <Toplists />
    <RidRow title="Inhoud van het Rijks ICT-dashboard">
      <PageBlock
        v-for="{ name, image, description, mainPage } in pageGroups"
        :key="name"
        class="mt-5"
        :title="name"
        :description="
          getContent(description.contentKey, description.contentName).value
        "
        :img-url="image.imgUrl"
        :img-author="image.imgAuthor"
        :sm="6"
        :lg="6"
        :align-links-to-bottom="false"
        :main-page="mainPage"
        :links="
          pages
            .filter((p) => p.groupName == name)
            .map(({ routeName, title: label }) => {
              return {
                routeName,
                label,
              }
            })
        "
      />

      <PageBlock
        v-for="p in pages.filter((p) => p.groupName == 'Overig')"
        :key="p.routeName"
        :title="p.title"
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
    <RidRow>
      <RidCol
        :md="12"
        :sm="12"
        :title-in-bar="false"
        title-level="h3"
        :fill-height="true"
        title="Samenvatting van ICT-activiteiten"
      >
        <PieChartOverview />
      </RidCol>
    </RidRow>
  </Page>
</template>

<script setup lang="ts">
import Page from "@/components/Page.vue"
import RidRow from "@/components/RidRow.vue"
import SearchBar from "@/views/SearchBar.vue"
import { pages, pageGroups } from "@/content/pages"
import PageBlock from "@/components/PageBlock.vue"
import { useTextLoader } from "@/composables/useTextLoader"
import Metrics from "@/views/Common/Metrics.vue"
import TextLoaderContent from "@/components/TextLoaderContent.vue"

const { getContent } = useTextLoader()
</script>

<style scoped lang="scss">
@import "@/styles/main.scss";
.home-image {
  background: linear-gradient(rgba(0, 0, 0, 0.35), rgba(0, 0, 0, 0.45)),
    url("/img/tweede-kamer-achtergrond-3.jpg");
  min-height: 325px;
  background-size: cover;
  background-position: 15% 25%;
}

.banner-content {
  max-width: 1200px;
}

.home-image-text {
  background-color: white;
  font-size: 0.9em;
  line-height: 1.5em;
}

.no-bottom-margin :deep(p) {
  margin-bottom: 0 !important;
}

:deep(.rich-content p) {
  max-width: 100%;
}
</style>
