/// <reference types="vite/client" />

declare module "vue-matomo"

declare module "*.md" {
  import type { ComponentOptions } from "vue"
  const Component: ComponentOptions
  export default Component
}
