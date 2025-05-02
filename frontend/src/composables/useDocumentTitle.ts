import { useTitle } from "@vueuse/core"

const defaultTitle = "Rijks ICT-dashboard"

const documentTitle = useTitle(defaultTitle)

const pageTitle = ref<string | undefined>(undefined)

watch(pageTitle, () => {
  documentTitle.value = pageTitle.value
    ? `${pageTitle.value} | ${defaultTitle}`
    : defaultTitle
})

export function useDocumentTitle() {
  return { pageTitle, defaultTitle }
}
