<template>
  <div class="px-4 py-3">
    {{ config.label }}

    <InformationIcon
      v-if="config.caption"
      :caption="config.caption"
      :label="config.label || ''"
    />
  </div>
  <ul class="list px-4">
    <li v-for="(row, index) in data" :key="index">
      <div
        v-for="attribute in config.attributes"
        :key="attribute.item"
        class="attribute"
      >
        <span v-if="attribute.type == 'string'" class="text">
          <span v-if="numbered" class="pr-2">{{ index + 1 }}.</span>
          <router-link
            v-if="linkConfig"
            :to="{
              name: linkConfig.name,
              params: {
                [linkConfig.routeIdKey]: row[linkConfig.idKey],
              },
            }"
            >{{ row[attribute.item] }}
          </router-link>
          <span v-else>{{ row[attribute.item as keyof typeof row] }}</span>
        </span>
        <span v-else-if="attribute.type === 'date'" class="date">
          {{
            dateToLocaleDateString(
              new Date(Date.parse(row[attribute.item] as string)),
            )
          }}
        </span>
      </div>
    </li>
  </ul>
</template>

<script setup lang="ts" generic="T extends Record<string, any>">
import { dateToLocaleDateString } from "@/util"
import type { ListConfig } from "@/types/project"

const props = defineProps<{
  numbered: boolean
  config: ListConfig<T>
  data: T[]
  linkConfig?: {
    name: string
    routeIdKey: string
    idKey: keyof T
  }
}>()

const config = toRef(props, "config")
const data = toRef(props, "data")
</script>

<style scoped>
.list li {
  display: flex;
  align-items: center;
  margin-bottom: 0.5em;
  justify-content: space-between;
}

.text {
  min-width: 51em;
}

.date {
  color: gray;
}
</style>
