import type { TextLoaderPayload, ContentPayload } from "@/types/textLoader"

import { getAllContent } from "@/services/textLoader"

const textLoaderPayload = ref<TextLoaderPayload | null>()

async function loadTextLoaderContent() {
  const data = await getAllContent()
  textLoaderPayload.value = data
  initialized.value = true
}

const getContent = (contentName: string, contentKey: keyof ContentPayload) => {
  if (!textLoaderPayload.value) loadTextLoaderContent()
  const contentMissing = `${contentName}.${contentKey} ontbreekt`
  return computed(() =>
    textLoaderPayload.value && textLoaderPayload.value.nl?.[contentName]
      ? textLoaderPayload.value.nl?.[contentName][contentKey]
      : contentMissing,
  )
}

const initialized = ref<boolean>(false)

export const useTextLoader = () => {
  return {
    loadTextLoaderContent,
    initialized,
    getContent,
  }
}

