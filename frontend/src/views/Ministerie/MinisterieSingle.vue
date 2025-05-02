<template>
  <AttributeDetail
    :attribute="'MinisterieNaam'"
    :attribute-value="ministerieNaam"
    attribute-label="Ministerie"
    :description="description"
  >
    <RidRow>
      <v-col :md="photoColWidth" :cols="12">
        <v-row>
          <template
            v-for="bewindspersoonType in bewindspersoonTypes"
            :key="bewindspersoonType"
          >
            <RidCol
              v-for="bewindspersoon in bewindspersonenMetType[
                bewindspersoonType
              ]"
              :key="bewindspersoon.naam"
              :cols="12"
              :sm="
                Math.floor(
                  12 /
                    (ministerieContent.minister.length +
                      (ministerieContent.staatssecretaris || []).length),
                )
              "
              :img="`/img/ministers/${bewindspersoon.naam}.jpg`"
              :img-title="`Portret van ${bewindspersoon.naam}`"
              :fill-height="true"
              :img-copyright-text="`Beeld: ${bewindspersoon.portretBron}`"
            >
              <h3 class="text-subtitle-1 font-weight-bold mb-0">
                {{
                  bewindspersoonType == "staatssecretaris"
                    ? "Staatssecretaris"
                    : "Minister "
                }}
              </h3>
              <p>{{ bewindspersoon.naam }}</p>
            </RidCol>
          </template>
        </v-row>
      </v-col>
      <v-col>
        <p
          v-for="o in ministerieContent.omschrijving"
          :key="o"
          class="mb-5 description"
        >
          {{ o }}
        </p>
      </v-col>
    </RidRow>
    <RidRow class="mb-8" title="Meer informatie"
      ><v-row>
        <v-col
          ><ul>
            <li v-if="!ministerieContent.hideIplan">
              Bekijk het
              <router-link
                :to="{
                  name: 'i-plan',
                }"
                >I-plan van {{ ministerieNaam }}</router-link
              >
            </li>
            <li>
              Lees meer over het ministerie op
              <a :href="ministerieContent.url" target="_blank"
                >de website van {{ ministerieNaam }}</a
              >
            </li>
          </ul></v-col
        >
      </v-row></RidRow
    >
  </AttributeDetail>
</template>

<script setup lang="ts">
import { getAggregation } from "@/services/project"
import { useContent } from "@/composables/useContent"
import type { Ministerie, Ministeries } from "@/types/content"
import RidRow from "@/components/RidRow.vue"
import RidCol from "@/components/RidCol.vue"
import AttributeDetail from "../AttributeDetail.vue"
import type { Bewindspersoon } from "@/types/content"
import { getObjectKeys } from "@/util"

const { content } = useContent()

const props = defineProps<{
  ministerieNaam: keyof Ministeries
}>()

const ministerieContent = computed(
  (): Ministerie => content.ministerie[props.ministerieNaam],
)

const nBewindspersonen = computed(
  () =>
    ministerieContent.value.minister.length +
    (ministerieContent.value.staatssecretaris || []).length,
)

const photoColWidth = computed(() => {
  if (nBewindspersonen.value == 1) {
    return 2
  } else if (nBewindspersonen.value < 3) {
    return 4
  } else {
    return 6
  }
})

const projectAggregatedByMinisterie = ref<Record<string, number> | null>(null)
const setprojectAggregatedByMinisterie = async () => {
  projectAggregatedByMinisterie.value = await getAggregation({
    attribute: "MinisterieNaam",
  })
}

setprojectAggregatedByMinisterie()

type BewindspersoonType = "minister" | "staatssecretaris"

const bewindspersonenMetType = computed(
  (): Record<BewindspersoonType, Bewindspersoon[]> => {
    return {
      minister: ministerieContent.value.minister,
      staatssecretaris: ministerieContent.value.staatssecretaris || [],
    }
  },
)

const bewindspersoonTypes = computed(() => {
  const obj = bewindspersonenMetType.value
  return getObjectKeys(obj)
})

const description = computed(() => ministerieContent.value.omschrijving[0])
</script>

<style scoped>
a {
  text-decoration: underline;
}

ul {
  padding-left: 50px;
}
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

.v-card:deep(.v-card-title) {
  white-space: normal !important;
  font-size: 0.95em;
}

.v-card:deep(.v-card-text) {
  white-space: normal !important;
  font-size: 1em;
}

div.v-card-text img {
  width: 100%;
  max-height: 250px;
}

.description {
  max-width: 800px;
}
</style>
