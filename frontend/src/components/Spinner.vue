<template>
  <div class="align-center">
    <v-progress-circular
      color="primary"
      indeterminate
      rounded
      size="50"
      role="progressbar"
      aria-label="progressiebar"
    />
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    size?: number
  }>(),
  { size: 50 },
)
</script>

<style scoped lang="scss">
.align-center {
  text-align: center;
}
</style>
