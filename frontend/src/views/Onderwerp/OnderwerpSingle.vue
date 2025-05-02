<template>
  <AttributeDetail
    attribute="Onderwerp"
    :attribute-value="onderwerp"
    attribute-label="Onderwerp"
    second-attribute="MaatschappelijkeBaat"
    second-attribute-slider-title="Wat ICT-activiteiten met dit onderwerp verbeteren"
    :description="description"
  >
    <RidRow>
      <v-col class="pt-0 description">
        <template
          v-for="({ subonderwerp, waarde }, index) in subonderwerpen"
          :key="subonderwerp"
        >
          <strong>{{ subonderwerp }}</strong>
          <p :class="index != subonderwerpen.length - 1 && 'pb-5'">
            {{ waarde }}
          </p>
        </template>

        <p class="mt-5">
          <a
            :href="content.onderwerp[onderwerp].urlRijksoverheid"
            target="_blank"
            rel="noopener"
            >Bekijk dit onderwerp op de website van de Rijksoverheid.</a
          >
        </p>
      </v-col>
    </RidRow>
  </AttributeDetail>
</template>

<script setup lang="ts">
import { useContent } from "@/composables/useContent"
import type { Onderwerpen } from "@/types/content"
import RidRow from "@/components/RidRow.vue"
import AttributeDetail from "../AttributeDetail.vue"
import type { OnderwerpenKey } from "@/types/content"

const { content } = useContent()

const props = defineProps<{ onderwerp: OnderwerpenKey }>()

const subonderwerpen = computed(() => {
  const onderwerp = content.onderwerp[props.onderwerp as keyof Onderwerpen]
  return onderwerp && onderwerp.subonderwerpen.length > 0
    ? onderwerp.subonderwerpen
    : []
})

const description = computed(() =>
  subonderwerpen.value.map((s) => s.waarde).join(" "),
)
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

.description {
  max-width: 800px;
}
</style>
