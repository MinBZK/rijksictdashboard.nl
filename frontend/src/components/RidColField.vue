<template>
  <v-col :cols="xs ? 12 : 6" class="pa-0">
    <v-card variant="flat">
      <template #title>
        <h3 class="text-subtitle-1 font-weight-bold ma-0">
          {{ title }}
        </h3>
      </template>

      <template #text>
        <slot />
      </template>
    </v-card>
  </v-col>
</template>

<script setup lang="ts">
import { useDisplay } from "vuetify"

const { xs } = useDisplay()

defineProps<{
  title: string
}>()
</script>

<style scoped lang="scss">
@import "@/styles/main.scss";
</style>
