<template>
  <TextLoaderContent
    class="mb-5"
    content-group="Maatschappelijke baten"
    content-field-key="content"
  />
  <v-expansion-panels v-model="expandedBaten" multiple class="mb-5">
    <v-expansion-panel
      v-for="baatItem in Object.keys(batenConfig)"
      :id="baatItem"
      :key="baatItem"
      class="custom-panel"
      rounded="0"
      elevation="0"
      bg-color="grey-lighten-5"
      :value="baatItem"
    >
      <v-expansion-panel-title> {{ baatItem }}</v-expansion-panel-title>
      <v-expansion-panel-text
        :ref="expandedBaten.includes(baatItem) ? 'selected' : 'unselected'"
      >
        <TextLoaderContent
          content-group="Maatschappelijke baten"
          :content-field-key="batenConfig[baatItem].toLowerCase()"
        />
        <ProjectManyTiles
          :filters="[
            {
              attribute: 'MaatschappelijkeBaat',
              values: [baatItem],
            },
          ]"
          title-level="h3"
        />
      </v-expansion-panel-text>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script setup lang="ts">
import TextLoaderContent from "@/components/TextLoaderContent.vue"
import ProjectManyTiles from "@/views/Project/ProjectManyTiles.vue"

const props = defineProps<{
  baat?: string
}>()

const batenConfig: Record<string, string> = {
  "Verbeterde dienstverlening": "Dienstverlening",
  Veiligheid: "Veiligheid",
  Compliance: "Compliance",
  Duurzaamheid: "Duurzaamheid",
  Efficiëntie: "Efficiëntie",
  Vakmanschap: "Vakmanschap",
  "Continuïteit van ICT": "Continuïteit",
}

const baat = toRef(props, "baat")
const expandedBaten = ref<string[]>([])

const scroll = () => {
  if (baat.value) {
    const scrollToElement = document.getElementById(baat.value)
    if (scrollToElement) scrollToElement.scrollIntoView({ behavior: "smooth" })
  }
}

onMounted(() => scroll())

watch(
  baat,
  () => {
    if (baat.value) {
      expandedBaten.value = [baat.value]
      // scroll()
    }
  },
  {
    immediate: true,
  },
)
</script>

<style scoped lang="scss">
@import "@/styles/_colors.scss";

.v-expansion-panel-title {
  font-size: 1.2em !important;
}
.custom-panel {
  border-bottom: 1px solid $grijs2;
  border-radius: 5px;
}
</style>
