<template>
  <page :title="`I-plan ${props.attributeValue}`">
    <template v-if="ministerieContent.iplanKey">
      <TextLoaderContent
        content-group="I-plannen"
        :content-field-key="ministerieContent.iplanKey"
      />
    </template>
    <template v-else>
      <div>
        <TextLoaderContent content-group="I-plannen" content-field-key="None" />
      </div>
    </template>
  </page>
</template>

<script setup lang="ts">
import page from "@/components/Page.vue"
import { useContent } from "@/composables/useContent"
import type { Ministeries } from "@/types/content"
import TextLoaderContent from "@/components/TextLoaderContent.vue"

const { content } = useContent()

const ministerieContent = computed(
  () => content.ministerie[props.attributeValue as keyof Ministeries],
)

const props = defineProps<{
  attributeValue: string
}>()
</script>
