<template>
  <v-tooltip
    v-model="show"
    location="top"
    max-width="500"
    :open-on-hover="false"
    :open-on-click="true"
    :no-click-animation="true"
    @click="show = !show"
    >{{ caption }}
    <template #activator="{ props }">
      <v-icon
        v-if="caption"
        v-click-outside="clickoutsideTooltip"
        color="primaryDark"
        v-bind="props"
        icon="mdi-information"
        size="20"
        tabindex="0"
        aria-label="Toon meer informatie over dit kengetal"
        role="button"
        :aria-expanded="show ? 'true' : 'false'"
        @keyup.esc="show = false"
        @keyup.enter="show = !show"
        @keyup.space="show = !show"
      />
    </template>
  </v-tooltip>
</template>

<script setup lang="ts">
defineProps<{
  caption: string
  label: string
}>()

const show = ref<boolean>(false)

const clickoutsideTooltip = () => {
  if (show.value) show.value = false
}
</script>
