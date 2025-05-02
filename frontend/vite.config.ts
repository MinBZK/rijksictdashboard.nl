import { fileURLToPath, URL } from "node:url"
import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue"
// https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vite-plugin
import vuetify from "vite-plugin-vuetify"
import Markdown from "vite-plugin-md"
import AutoImport from "unplugin-auto-import/vite"
import Components from "unplugin-vue-components/vite"

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue({ include: [/\.vue$/, /\.md$/] }),
    AutoImport({ imports: ["vue", "vue-router"], eslintrc: { enabled: true } }),
    vuetify({ autoImport: true }),
    Markdown(),
    Components({ dirs: ["src/components", "src/views"] }),
  ],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
})
