<template>
  <Head>
    <title>{{ headTitle }}</title>
    <meta name="description" :content="description" />
    <link rel="canonical" :href="fullUrl" />
  </Head>

  <Breadcrumb v-if="!contentOnly" />
  <slot name="page-before"></slot>

  <Teleport to="#drawer">
    <v-navigation-drawer
      v-model="drawer"
      width="350"
      location="left"
      :disable-route-watcher="true"
      temporary
    >
      <slot name="drawer" />
    </v-navigation-drawer>
  </Teleport>

  <v-container :class="['main-container', textOnly ? 'small-text' : '']">
    <v-row v-if="error">
      <v-alert type="error" variant="outlined">
        {{ error }}
      </v-alert>
    </v-row>

    <slot name="content-before"></slot>

    <div id="content" class="page">
      <div>
        <h1 class="mb-4">{{ title }}</h1>
        <h2 v-if="subtitle" class="subtitle">{{ subtitle }}</h2>

        <slot />
        <slot name="after" />
      </div>
    </div>
    <div v-if="!error && loading" id="content" class="align-center pt-10">
      <SpinnerVue :size="100" />
    </div>
  </v-container>
</template>

<script setup lang="ts">
import Breadcrumb from "@/components/Breadcrumb.vue"
import { useGlobalStore } from "@/store/useGlobalStore"
import SpinnerVue from "@/components/Spinner.vue"
import { Head } from "@unhead/vue/components"

const { contentOnly } = useGlobalStore()

interface Props {
  title: string
  titleCategory?: string
  subtitle?: string
  minHeight?: number
  scrollToContent?: boolean
  loading?: boolean
  error?: string
  showDrawer?: boolean
  description?: string
  className?: string
  textOnly?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  scrollToContent: true,
  loading: false,
  showDrawer: false,
  description:
    "Op het Rijks ICT-dashboard vindt u informatie over hoe de Rijksoverheid werkt aan het verbeteren van de digitalisering. Onderdelen hiervan zijn de I-strategie, de grote ICT-activiteiten, duurzaamheid binnen de Rijksoverheid en de kosten en resultaten van ICT. Zo draagt het Rijks ICT-dashboard bij aan een open overheid",
})

const minHeightFinal = computed(() => {
  return `${props.minHeight || window.innerHeight - 300}px`
})

const timeout = (ms: number) =>
  new Promise((resolve) => setTimeout(resolve, ms))

const title = toRef(props, "title")
const titleCategory = computed(() => props.titleCategory)
const showDrawer = toRef(props, "showDrawer")
const drawer = ref<boolean>(false)

const emit = defineEmits<{
  (e: "closeDrawer"): void
}>()
watch(showDrawer, () => {
  drawer.value = showDrawer.value
})
watch(drawer, () => {
  if (!drawer.value) emit("closeDrawer")
})

const scroll = () => {
  const scrollToElementId = props.scrollToContent ? "bar" : "app"
  const scrollToElement = document.getElementById(scrollToElementId)
  if (scrollToElement && props.scrollToContent)
    scrollToElement.scrollIntoView({ behavior: "smooth" })
}

onMounted(async () => {
  ;(document.activeElement as HTMLElement).blur()
  await timeout(50)
  await nextTick()
  scroll()
})

const headTitle = computed(() => {
  if (titleCategory.value) {
    return `${title.value} | ${titleCategory.value}`
  } else {
    return title.value
  }
})

watch(
  [headTitle],
  () => {
    scroll()
  },
  {
    immediate: true,
  },
)

const route = useRoute()
const fullUrl = computed(() => `https://${window.location.host}${route.path}`)
</script>

<style scoped lang="scss">
@import "@/styles/main.scss";
.main-container {
  max-width: 1200px;
}

.v-row {
  margin: 0 !important;
}

#main {
  min-height: v-bind(minHeightFinal);
  padding-left: 0 !important;
}

h2 {
  font-weight: normal;
  font-size: 85% !important;
  margin-top: -1em;
}

.align-center {
  justify-content: center;
}

.small-text {
  max-width: 800px;
}
</style>
