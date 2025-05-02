// Styles
import "@mdi/font/css/materialdesignicons.css"
import "vuetify/styles"
import { nl } from "vuetify/locale"
import colors from "@/config/colors"
// Vuetify
import { createVuetify } from "vuetify"

const variables = {
  "border-color": "#000000",
  "border-opacity": 0.12,
  "high-emphasis-opacity": 1,
  "medium-emphasis-opacity": 0.6,
  "disabled-opacity": 0.38,
  "idle-opacity": 0.04,
  "hover-opacity": 0.04,
  "focus-opacity": 0.12,
  "selected-opacity": 0.08,
  "activated-opacity": 0.12,
  "pressed-opacity": 0.12,
  "dragged-opacity": 0.08,
  "kbd-background-color": "#212529",
  "kbd-color": "#FFFFFF",
  "code-background-color": "#C2C2C2",
}

const theme = {
  cspNonce: "eQw4j9WgXcB",
  themes: {
    light: {
      dark: false,
      colors,
      variables,
    },
  },
}

export default createVuetify({
  theme,
  locale: {
    locale: "nl",
    messages: { nl },
  },
})
