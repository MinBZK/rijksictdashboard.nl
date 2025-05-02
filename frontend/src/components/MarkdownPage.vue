<template>
  <page :title="props.label">
    <component :is="currentMarkdown" class="markdown-content" />
  </page>
</template>

<script setup lang="ts">
import Page from "@/components/Page.vue"

const props = defineProps<{ label: string; slug: string }>()

const currentMarkdown = shallowRef("")

const setMarkdownComponent = () => {
  const newMarkdown = defineAsyncComponent(
    () => import(`@/content/md/${props.slug}.md`),
  )
  currentMarkdown.value = newMarkdown
}

setMarkdownComponent()

watch(
  () => props.slug,
  () => {
    setMarkdownComponent()
  },
)
</script>

<style>
.markdown-content p {
  margin-bottom: 0.5em;
}

.markdown-content ol,
.markdown-content ul {
  margin-bottom: 1em;
}

.markdown-content a:before {
  display: inline-flex;
  align-items: center;
  left: 1px;
  top: 0;
  height: 22.4px;
}

.markdown-content li {
  margin-left: 1.5em;
}

/*
@media(min-width: 768px) {
  .article p a.external:before,.article li a.external:before {
      top:-1px
  }
}

@media(min-width: 992px) {
  .article p a.external:before,.article li a.external:before {
      top:-2px
  }
}

@media(min-width: 768px) {
  .article p a.external:before,.article li a.external:before {
      height:25.2px
  }
}

@media(min-width: 992px) {
  .article p a.external:before,.article li a.external:before {
      height:28px
  }
}
 */
</style>
