import { createRouter, createWebHistory } from "vue-router"
import generalRoutes from "@/router/general"
import footerRoutes from "@/router/footer"
import "vue-router"

declare module "vue-router" {
  interface RouteMeta {
    parentRouteName?: string
    label?: string
  }
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    ...generalRoutes,
    ...footerRoutes,
    {
      path: "/:pathMatch(.*)*",
      name: "catchAll",
      redirect: {
        name: "pageNotFound",
      },
    },
  ],
})

export default router
