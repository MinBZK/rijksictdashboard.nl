<template>
  <v-app>
    <div id="drawer" />
    <template v-if="!contentOnly">
      <ScreenreaderMessageLiveArea
        >{{ pageDescription }}
      </ScreenreaderMessageLiveArea>
      <div class="skiplinks">
        <a href="#content">Ga direct naar inhoud</a>
      </div>

      <RijksoverheidHeaderVue :title="defaultTitle" />

      <v-main>
        <router-view v-slot="{ Component }">
          <component :is="Component" v-if="initialized" />
        </router-view>
      </v-main>

      <RijksoverheidFooter />
    </template>
    <template v-if="contentOnly"
      ><router-view />

      <router-view name="content-after" />
    </template>
  </v-app>
</template>

<script setup lang="ts">
import RijksoverheidHeaderVue from "./components/Header.vue"
import RijksoverheidFooter from "./components/Footer.vue"
import { useGlobalStore } from "@/store/useGlobalStore"
import { useTextLoader } from "./composables/useTextLoader"
import { useDocumentTitle } from "./composables/useDocumentTitle"
import { useRoute } from "vue-router"
import ScreenreaderMessageLiveArea from "@/components/ScreenreaderMessageLiveArea.vue"

const { pageTitle, defaultTitle } = useDocumentTitle()

const route = useRoute()

const pageDescription = ref<string>("")

watch(pageTitle, (newTitle, oldTitle) => {
  const extraInformatie =
    (route.meta["screenreaderDescription"] as string) || ""

  const structuurDescription = `Schermlezerinformatie: ${
    extraInformatie || "geen bijzonderheden op deze pagina."
  }`

  if (newTitle !== oldTitle && newTitle !== undefined) {
    pageDescription.value =
      route.name == "home"
        ? "Je bent nu op de homepagina"
        : `Je bent nu op de pagina: '${pageTitle.value}'. ` +
          structuurDescription
  }
})

const { contentOnly } = useGlobalStore()

const { initialized, loadTextLoaderContent } = useTextLoader()
loadTextLoaderContent()
// init()
</script>
