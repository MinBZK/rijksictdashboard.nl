import footer from "@/config/footer"
import type { FooterPage } from "@/config/footer"
import type { RouteRecordRaw } from "vue-router"

export default footer
  .reduce((pages, footerColumn) => {
    return [...pages, ...footerColumn.pages]
  }, [] as FooterPage[])
  .filter(({ addToRouter, component }) => addToRouter !== false && component)
  .map(({ label, slug, component }) => {
    return {
      path: `/${slug}`,
      name: label,
      component,
      meta: {
        parentRouteName: "home",
      },
    }
  }) as RouteRecordRaw[]
