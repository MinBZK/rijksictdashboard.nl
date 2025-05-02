<template>
  <TileSlider
    :slider-data="sliderData"
    :title="`${title} (${sliderData.length})`"
    :title-level="titleLevel"
  />
</template>

<script setup lang="ts">
import { getMany } from "@/services/project"
import type { Project } from "@/api-new"
import type { ProjectFilter } from "@/types/project"
import TileSlider from "@/components/TileSlider.vue"
import type { TitleLevel } from "@/types/components"
import type { TileSliderData } from "@/types/components"
import type { RouteLocationRaw } from "vue-router"

const props = withDefaults(
  defineProps<{
    currentProjectId?: string
    filters?: ProjectFilter[]
    title?: string
    titleLevel?: TitleLevel
    projecten?: Project[]
  }>(),
  {
    title: "ICT-activiteiten",
    titleLevel: "h2",
  },
)

const projectenLoaded = ref<Project[]>([])

const projectenFinal = computed(() => props.projecten || projectenLoaded.value)

const getProjecten = async () => {
  const { results } = await getMany({
    filters: JSON.stringify(props.filters || []),
  })

  projectenLoaded.value = results
}

const emit = defineEmits<{
  (e: "receivedProjectCount", count: number): void
}>()

const sliderData = computed(() =>
  projectenFinal.value
    .filter((p) =>
      props.currentProjectId ? p.ProjectId !== props.currentProjectId : true,
    )
    .map((p): TileSliderData => {
      return {
        title: p.Naam,
        subtitle: p.ProjectStatus || undefined,
        route: {
          name: "ict-activiteit",
          params: { projectId: p.ProjectId, slug: p.Slug },
        } as RouteLocationRaw,
      }
    }),
)

watch(
  props,
  () => {
    if (!props.projecten) {
      getProjecten()
    }
  },
  { immediate: true },
)
watch(projectenFinal, () => {
  emit("receivedProjectCount", projectenLoaded.value.length)
})
</script>

<style scoped>
.page-desription-text {
  background-color: rgb(248, 248, 248);
}

.slider-text {
  display: table-cell;
  width: 250px;
  height: 200px;
  padding: 10px;
  vertical-align: middle;
  text-align: center;
  font-size: 18px;
  color: rgb(83, 83, 83);
}
</style>
