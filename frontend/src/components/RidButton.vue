<template>
  <v-btn
    ref="button"
    color="primaryDark"
    variant="tonal"
    rounded="0"
    class="text-none no-overlay"
  >
    <slot />
  </v-btn>
</template>

<script setup lang="ts">
const button = ref(null)

const focus = () => {
  // @ts-ignore
  button.value?.$el?.focus()
}

defineExpose({
  focus,
})
</script>

<style scoped lang="scss">
:deep(.v-btn__content) {
  letter-spacing: normal;
  font-size: 1.2em;
}
.v-btn:focus {
  outline: 2px dashed #000;
  outline-offset: 4px;
  z-index: 1;
}

.v-btn {
  --v-theme-overlay-multiplier: 0.2;
}

.v-btn:hover {
  --v-theme-overlay-multiplier: 1;
}
</style>
