<template>
  <template v-if="multilineValue.length > 1">
    <template v-for="(v, index) in multilineValue" :key="v">
      {{ v }}
      <br v-if="index < multilineValue.length - 1" />
    </template>
  </template>
  <template v-else>{{ value }}</template>
</template>

<script setup lang="ts">
const props = defineProps<{
  value: string
}>()

const multilineValue = computed(() => {
  const v = props.value
  return v.split(/\r?\n/)
})
</script>
