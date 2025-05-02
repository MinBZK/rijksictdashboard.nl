import App from "./App.vue"
import vuetify from "./plugins/vuetify"
import router from "./router"
import { createPinia } from "pinia"
import PrimeVue from "primevue/config"
import Dropdown from "primevue/dropdown"
import MultiSelect from "primevue/multiselect"
import axios from "axios"
import "./styles/main.scss"
import { getApiBaseUrl } from "./util"
// import VueMatomo from "vue-matomo"
import "@/styles/primevue.css"
import locale from "@/config/accessability-locale"
import { createHead } from "@unhead/vue"

const head = createHead()

const pinia = createPinia()

// const matomoConfig = {
//   host: "https://statistiek.rijksoverheid.nl",
//   siteId: "<YOUR_SITE_ID>",
//   trackerFileName: "matomo",
//   router,
//   enableLinkTracking: true,
//   requireConsent: false,
//   trackInitialView: true,
//   disableCookies: false,
//   requireCookieConsent: false,
//   enableHeartBeatTimer: false,
//   heartBeatTimerInterval: 15,
//   debug: false,
//   userId: undefined,
//   cookieDomain: undefined,
//   domains: undefined,
//   preInitActions: [],
//   trackSiteSearch: false,
// }

console.log("Mode: " + import.meta.env.MODE)

axios.defaults.baseURL = getApiBaseUrl()

const app = createApp(App).use(pinia).use(router).use(vuetify)

// When adding or changing anything Primevue related, ensure that the CSP still works.
// The (CSP) content security policy is a header set by Nginx. Nginx is configured in the Dockerfile in /frontend.
// Steps to take when adjusting anything Primevue related:

// 1. Make build using 'npm run build-dev'
// 2. Run the build using the Nginx image (service 'dashboard' in docker-compose.yml)
// 3. Verify in the console that there are no CSP errors. If so, copy paste the sha256 hash from the error message and add it the CSP in frontend/nginx.conf.

app.use(PrimeVue, {
  locale,
})
app.use(head)
app.component("PrimeDropdown", Dropdown)
app.component("PrimeMultiSelect", MultiSelect)


app.mount("#app")
