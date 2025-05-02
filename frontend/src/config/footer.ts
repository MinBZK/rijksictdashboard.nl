import type { Component } from "vue"
import Over from "@/views/Footer/Over.vue"
import RapportageGeschiedenis from "@/views/Footer/Rapportagegeschiedenis.vue"
import Privacy from "@/views/Footer/Privacy.vue"
import Copyright from "@/views/Footer/Copyright.vue"
import Contact from "@/views/Footer/Contact.vue"
import Cookies from "@/views/Footer/Cookies.vue"
import Toegankelijkheid from "@/views/Footer/Toegankelijkheid.vue"
import KwetsbaarheidMelden from "@/views/Footer/KwetsbaarheidMelden.vue"
import Sitemap from "@/views/Footer/Sitemap.vue"
import ReleaseNotes from "@/views/Footer/ReleaseNotes.vue"
import Archief from "@/views/Footer/Archief.vue"

export type FooterPage = {
  label: string
  slug: string
  addToRouter?: boolean
  component?: Component
}

export type FooterColumn = {
  title: string
  pages: FooterPage[]
}

const footer: FooterColumn[] = [
  {
    title: "Service",
    pages: [
      {
        label: "Contact",
        slug: "contact",
        component: Contact,
      },

      {
        label: "Sitemap",
        slug: "sitemap",
        component: Sitemap,
      },
      {
        label: "Open data",
        slug: "open-data",
        addToRouter: false,
      },
      {
        label: "Versie-informatie",
        slug: "versie-informatie",
        component: ReleaseNotes,
      },
      {
        label: "Rapportagegeschiedenis",
        slug: "rapportagegeschiedenis",
        component: RapportageGeschiedenis,
      },
    ],
  },
  {
    title: "Over deze site",
    pages: [
      {
        label: "Over",
        slug: "over",
        component: Over,
      },
      {
        label: "Privacy",
        slug: "privacy",
        component: Privacy,
      },
      {
        label: "Archief",
        slug: "archief",
        component: Archief,
      },
      {
        label: "Cookies",
        slug: "cookies",
        component: Cookies,
      },
      {
        label: "Copyright",
        slug: "copyright",
        component: Copyright,
      },
      {
        label: "Toegankelijkheid",
        slug: "toegankelijkheid",
        component: Toegankelijkheid,
      },
      {
        label: "Kwetsbaarheid melden",
        slug: "kwetsbaarheid-melden",
        component: KwetsbaarheidMelden,
      },
    ],
  },
]

export default footer
