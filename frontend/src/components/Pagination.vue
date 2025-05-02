<template>
  <div class="pagination">
    <div v-if="totalCount > 0" class="pagination-info">
      {{ title }}
      {{ startIndex }} - {{ endIndex }} van
      {{ totalCount }}
    </div>
    <div class="pagination-buttons no-overlay">
      <v-btn
        icon="mdi-page-first"
        variant="plain"
        aria-label="Ga naar eerste pagina"
        :disabled="page == 1"
        :aria-hidden="page == 1"
        color="primary"
        class="mr-0"
        @click="goToPage(1)"
        @keydown.enter="goToPage(1)"
      ></v-btn>
      <v-btn
        icon="mdi-chevron-left"
        variant="plain"
        aria-label="Ga naar vorige pagina"
        :disabled="page == 1"
        :aria-hidden="page == 1"
        color="primary"
        class="mr-0"
        @click="goToPage(page - 1)"
        @keydown.enter="goToPage(page - 1)"
      ></v-btn>
      <v-btn
        icon="mdi-chevron-right"
        variant="plain"
        aria-label="Ga naar volgende pagina"
        color="primary"
        :disabled="page == nPages"
        :aria-hidden="page == nPages"
        class="mr-0"
        @click="goToPage(page + 1)"
        @keydown.enter="goToPage(page + 1)"
      ></v-btn>
      <v-btn
        icon="mdi-page-last"
        color="primary"
        variant="plain"
        aria-label="Ga naar laatste pagina"
        :disabled="page == nPages"
        :aria-hidden="page == nPages"
        class="mr-0"
        @click="goToPage(nPages)"
        @keydown.enter="goToPage(nPages)"
      ></v-btn>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  title?: string
  totalCount: number
  pageLength: number
  scrollToTop?: boolean
  topOffset?: number
}>()

const nPages = computed(() => Math.ceil(props.totalCount / props.pageLength))

const page = defineModel<number>("page", { default: 1 })

const emit = defineEmits<{
  (e: "updatePage", page: number): void
}>()

const goToPage = (targetPage: number) => {
  page.value = targetPage
  emit("updatePage", targetPage)
  if (props.scrollToTop) {
    scrollToTop()
  }
}

const scrollToTop = () => {
  window.scrollTo({
    top: props.topOffset || 0,
    behavior: "smooth",
  })
}

const startIndex = computed(() => (page.value - 1) * props.pageLength + 1)

const endIndex = computed(() => {
  return (
    (page.value - 1) * props.pageLength +
    (page.value == nPages.value
      ? props.totalCount % props.pageLength
      : props.pageLength)
  )
})
</script>

<style scoped lang="scss">
@import "@/styles/_colors.scss";

.pagination {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}
.pagination-info {
  display: flex;
  color: $grijs7;
}
.v-btn--variant-flat {
  color: $primary !important;
}
.pagination .v-btn {
  padding: 0;
}
.pagination-buttons {
  margin-left: 1em;
}
.v-btn:focus {
  outline: 2px dashed #000;
  outline-offset: 4px;
}
</style>
