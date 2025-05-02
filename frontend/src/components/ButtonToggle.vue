<script setup lang="ts">
defineProps<{
  options: string[]
}>()

const selectedOption = defineModel<string>({
  required: true,
})
</script>

<template>
  <div class="text-center">
    <RidButton
      v-for="(c, index) in options"
      :key="c"
      :class="{
        'button-toggle': index != options.length - 1,
        toggled: selectedOption == c,
      }"
      :aria-current="selectedOption == c ? 'true' : 'false'"
      variant="flat"
      :color="selectedOption == c ? 'primaryDark' : 'tertiary'"
      :value="c"
      @click="selectedOption = c"
      >{{ c }}</RidButton
    >
  </div>
</template>

<style lang="css" scoped>
.button-toggle {
  border-right-width: 0;
}
</style>
