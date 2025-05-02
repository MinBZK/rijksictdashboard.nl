<template>
  <v-dialog
    ref="dialogElement"
    v-model="show"
    :max-width="maxWidth"
    scrollable
    role="dialog"
    aria-labelledby="dialogTitle"
    aria-describedby="dialogText"
  >
    <v-card>
      <v-card-title v-if="title" id="dialogTitle">
        <h1 class="mb-0 text-h5">{{ title }}</h1>
      </v-card-title>
      <v-divider v-if="title"></v-divider>

      <v-card-text id="dialogText" class="text-small">
        <template v-if="content && typeof content === 'string'">
          <FormattedValueMultilineString :value="content" />
        </template>
        <template v-else-if="content">
          {{ content }}
        </template>
        <slot />
      </v-card-text>
      <v-divider></v-divider>

      <v-card-actions>
        <slot name="actions">
          <RidButton
            ref="button"
            color="primaryDark"
            block
            @click="show = false"
            >Sluiten</RidButton
          >
        </slot>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import FormattedValueMultilineString from "./FormattedValueMultilineString.vue"
import RidButton from "@/components/RidButton.vue"

const props = withDefaults(
  defineProps<{
    content?: string | number
    title: string
    maxWidth?: string
    returnFocus?: CallableFunction
  }>(),
  {
    maxWidth: "800",
  },
)

const show = ref<boolean>(true)

const emit = defineEmits<{
  (e: "close"): void
}>()

watch(show, async () => {
  if (props.returnFocus) {
    await nextTick()
    props.returnFocus()
  }
  emit("close")
})

const button = ref<HTMLElement | null>(null)
onMounted(() => {
  button.value?.focus()
})
</script>

<style scoped="scss">
.text-small {
  font-size: 0.9em !important;
}

.v-card-text {
  letter-spacing: normal !important;
}

div {
  line-height: 1.5em !important;
}

div#dialogText {
  max-height: 70vh;
}

div#dialogTitle {
  white-space: normal;
  word-wrap: break-word;
}
</style>
