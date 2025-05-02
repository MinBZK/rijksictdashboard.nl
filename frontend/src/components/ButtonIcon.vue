<template>
  <span
    ref="button"
    role="button"
    tabindex="0"
    :class="colored && 'button-link'"
    ><v-icon>{{ icon }}</v-icon></span
  >
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    icon: string
    colored?: boolean
  }>(),
  {
    colored: true,
  },
)

const button = ref<HTMLElement | null>(null)

const focus = () => button.value?.focus()

defineExpose({
  focus,
})
</script>

<style lang="scss" scoped>
@import "@/styles/_colors.scss";

.button-link {
  color: $primary;
}
</style>
