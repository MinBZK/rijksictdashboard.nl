import Home from "@/views/Home.vue"
import IctActiviteiten from "@/views/Project/ProjectMany.vue"
import Project from "@/views/Project/ProjectSingle.vue"
import Ministeries from "@/views/Ministerie/MinisterieMany.vue"
import Ministerie from "@/views/Ministerie/MinisterieSingle.vue"
import Dienstverlening from "@/views/Dienstverlening/DienstverleningSingle.vue"

import Onderwerp from "@/views/Onderwerp/OnderwerpSingle.vue"
import Onderwerpen from "@/views/Onderwerp/OnderwerpMany.vue"
import type { RouteRecordRaw } from "vue-router"
import Over from "@/views/Footer/Over.vue"
import PageNotFound from "@/views/PageNotFound.vue"
import type { AttributeSorting, ProjectFilter } from "@/types/project"
import { parseRouteQueryString } from "@/util/querystring"
import IPlan from "@/views/IPlan/IPlanSingle.vue"
import SoortSingle from "@/views/SoortActiviteit/SoortSingle.vue"

// pages
import ContextPage from "@/views/ContextPage.vue"
import TextLoaderPage from "@/views/Pages/TextLoaderPage.vue"
import IctKosten from "@/views/Pages/IctKosten.vue"
import Baten from "@/views/Pages/Baten.vue"
import Duurzaamheid from "@/views/Pages/Duurzaamheid.vue"
import AlgoritmesEnAI from "@/views/Pages/AlgoritmesEnAI.vue"
import Informatiehuishouding from "@/views/Pages/InformatieHuishouding.vue"
import IctMedewerkers from "@/views/Pages/IctMedewerkers.vue"
import Dashboard from "@/views/Pages/Dashboard.vue"
import OpenData from "@/views/Footer/OpenData.vue"
import Istrategie from "@/views/Pages/I-strategie.vue"
import Search from "@/views/Pages/Zoekresultaten.vue"

const routes: RouteRecordRaw[] = [
  {
    path: "/",
    name: "home",
    component: Home,
    meta: {
      screenreaderDescription:
        "Met het zoekveld kun je snel navigeren naar een ICT-activiteit, een ministerie of een onderwerp.",
    },
  },
  {
    path: "/ict-activiteiten",
    name: "ICT-activiteiten",
    component: IctActiviteiten,
    meta: {
      label: "Grote ICT-activiteiten",
      parentRouteName: "home",
      screenreaderDescription:
        "Met het invoerveld kun je het ICT-activiteit overzicht filteren op naam. Het overzicht van ICT-activiteiten wordt direct geüpdatet. De ICT-activiteiten kunnen ook gefilterd worden middels keuzelijsten. ",
    },
    props: (route) => {
      const page = route.query.page?.toString()

      return {
        page: page ? parseInt(page) : undefined,
        filters: parseRouteQueryString(
          route.query.filters?.toString(),
          "f",
        ) as ProjectFilter[],
        sorting: parseRouteQueryString(
          route.query.sorting?.toString(),
          "s",
        ) as AttributeSorting[],
        search: route.query.search || "",
      }
    },
  },
  {
    path: "/projecten/:legacyProjectId/:slug?",
    component: Project,
    props: (route) => ({
      legacyProjectId: route.params.legacyProjectId,
    }),
    meta: {
      parentRouteName: "ICT-activiteiten",
      screenreaderDescription:
        "Deze pagina bevat een grafiek. Er is ook een datatabel beschikbaar.",
    },
  },
  {
    name: "ict-activiteit",
    path: "/ict-activiteiten/:projectId/:slug?",
    component: Project,
    props: (route) => ({
      projectId: route.params.projectId,
    }),
    meta: {
      parentRouteName: "ICT-activiteiten",
      screenreaderDescription:
        "Deze pagina bevat een grafiek. Er is ook een datatabel beschikbaar.",
    },
  },
  {
    path: "/onderwerpen",
    name: "onderwerpen",
    component: Onderwerpen,
    meta: {
      parentRouteName: "home",
    },
  },
  {
    path: "/onderwerpen/:attributeValue",
    name: "onderwerp",
    props: (route) => {
      return {
        onderwerp: route.params.attributeValue,
      }
    },
    component: Onderwerp,
    meta: {
      parentRouteName: "onderwerpen",
    },
  },
  {
    path: "/ministeries",
    name: "ministeries",
    component: Ministeries,
    meta: {
      parentRouteName: "home",
    },
  },
  {
    path: "/ministeries/:attributeValue",
    name: "ministerie",
    props: (route) => {
      return {
        ministerieNaam: route.params.attributeValue,
      }
    },
    component: Ministerie,
    meta: {
      parentRouteName: "ministeries",
    },
  },
  {
    path: "/dienstverlening/:attributeValue",
    name: "dienstverlening",
    props: (route) => {
      return {
        dienstverlening: route.params.attributeValue,
      }
    },
    component: Dienstverlening,
    meta: {
      parentRouteName: "home",
    },
  },
  {
    path: "/soort/:attributeValue",
    name: "soort",
    props: (route) => {
      return {
        soort: route.params.attributeValue,
      }
    },
    meta: {
      parentRouteName: "home",
    },
    component: SoortSingle,
  },
  {
    path: "/ministeries/:attributeValue/i-plan",
    name: "i-plan",
    props: true,
    component: IPlan,
    meta: {
      parentRouteName: "ministerie",
    },
  },
  {
    path: "/duurzaamheid",
    component: ContextPage,
    props: {
      hidePreview: true,
      expandable: false,
    },
    children: [
      {
        path: "",
        name: "duurzaamheid",
        component: Duurzaamheid,
        meta: {
          parentRouteName: "home",
          screenreaderDescription:
            "Deze pagina bevat een grafiek. Er is ook een data tabel beschikbaar.",
        },
      },
    ],
  },
  {
    path: "/ict-kosten",
    component: ContextPage,
    props: {
      hidePreview: true,
      expandable: false,
    },
    children: [
      {
        path: "",
        name: "ICT-kosten",
        component: IctKosten,
        meta: {
          parentRouteName: "home",
          screenreaderDescription:
            "Deze pagina bevat grafieken, voor elke grafiek is er een data tabel beschikbaar. De informatie in deze grafieken kun je filteren op ministerie en/of jaar middels keuzelijsten.",
        },
      },
    ],
  },
  {
    path: "/open-data",
    component: ContextPage,
    props: {
      expandable: false,
    },
    children: [
      {
        path: "",
        name: "Open data",
        component: OpenData,
        meta: {
          parentRouteName: "home",
        },
      },
    ],
  },
  {
    path: "/over",
    name: "over",
    component: Over,
    meta: {
      parentRouteName: "home",
    },
  },
  {
    path: "/i-strategie",
    component: ContextPage,
    props: {
      hidePreview: true,
      expandable: false,
    },
    children: [
      {
        path: "",
        name: "i-strategie",
        component: Istrategie,
        meta: {
          parentRouteName: "home",
        },
      },
    ],
  },
  {
    path: "/ict-medewerkers",
    component: ContextPage,
    props: {
      hidePreview: true,
      expandable: false,
    },
    children: [
      {
        path: "",
        name: "ICT-medewerkers",
        component: IctMedewerkers,
        meta: {
          parentRouteName: "home",
          screenreaderDescription:
            "Deze pagina bevat een grafiek. Er is ook een datatabel beschikbaar. De informatie in de grafiek kun je filteren op ministerie middels een keuzelijst.",
        },
      },
    ],
  },
  {
    path: "/kengetallen-ict-activiteiten",
    component: ContextPage,
    props: {
      expandable: false,
      hidePreview: true,
    },
    children: [
      {
        path: "",
        name: "Dashboard",
        component: Dashboard,
        meta: {
          parentRouteName: "home",
          screenreaderDescription:
            "De informatie op deze pagina kun je filteren op ministerie middels een keuzelijst. Deze pagina bevat grafieken, voor elke grafiek is er een data tabel beschikbaar.",
        },
      },
    ],
  },
  {
    path: "/algoritmes-en-ai",
    component: ContextPage,
    props: {
      hidePreview: true,
      expandable: false,
    },
    children: [
      {
        path: "",
        name: "Algoritmes en AI",
        component: AlgoritmesEnAI,
        meta: {
          parentRouteName: "home",
        },
      },
    ],
  },
  {
    path: "/architectuur",
    component: ContextPage,
    props: {
      expandable: false,
    },
    children: [
      {
        path: "",
        name: "Architectuur",
        component: TextLoaderPage,
        props: {
          contentGroup: "Architectuur",
          contentKey: "content",
        },
        meta: {
          parentRouteName: "home",
        },
      },
    ],
  },
  {
    path: "/it-assetmanagement",
    component: ContextPage,
    props: {
      expandable: false,
    },
    children: [
      {
        path: "",
        name: "IT-Assetmanagement",
        component: TextLoaderPage,
        props: {
          contentGroup: "Softwarekwaliteit",
          contentKey: "content",
        },
        meta: {
          parentRouteName: "home",
        },
      },
    ],
  },
  {
    path: "/informatiehuishouding",
    component: ContextPage,
    props: {
      hidePreview: true,
      expandable: false,
    },
    children: [
      {
        path: "",
        name: "Informatiehuishouding",
        component: Informatiehuishouding,
        meta: {
          parentRouteName: "home",
        },
      },
    ],
  },
  {
    path: "/informatiebeveiliging",
    component: ContextPage,
    props: {
      expandable: false,
    },
    children: [
      {
        path: "",
        name: "Informatiebeveiliging",
        component: TextLoaderPage,
        props: {
          contentGroup: "Informatiebeveiliging",
          contentKey: "content",
        },
        meta: {
          parentRouteName: "home",
        },
      },
    ],
  },
  {
    path: "/wat-we-verbeteren",
    component: ContextPage,
    props: {
      expandable: false,
    },
    children: [
      {
        path: "",
        name: "wat we verbeteren",
        component: Baten,
        meta: {
          parentRouteName: "home",
          screenreaderDescription:
            "Deze pagina bevat zeven thema's waar de Rijksoverheid op wil verbeteren. Je kunt ook zien welke ICT-activiteiten er bijdragen aan de verbetering van deze thema's.",
        },
      },
      {
        path: ":attributeValue",
        name: "wat we verbeteren detail",
        component: Baten,
        props: (route) => {
          return {
            baat: route.params.attributeValue,
          }
        },
        meta: {
          parentRouteName: "home",
        },
      },
    ],
  },
  {
    path: "/zoekresultaten",
    name: "zoekresultaten",
    component: Search,
    props: (route) => ({
      searchType: route.query.searchType,
      searchQuery: route.query.searchQuery,
      category: route.query.category,
    }),
    meta: {
      parentRouteName: "home",
    },
  },
  // {
  //   path: "/wat-we-verbeteren/:attributeValue",
  //   component: ContextPage,
  //   children: [
  //     {
  //       path: "",
  //       name: "wat we verbeteren detail",
  //       component: Baten,
  //       props: (route) => {
  //         return {
  //           baat: route.params.attributeValue,
  //         }
  //       },
  //       meta: {
  //         parentRouteName: "home",
  //       },
  //     },
  //   ],
  // },
  {
    path: "/pagina-niet-gevonden",
    name: "pageNotFound",
    component: PageNotFound,
  },
]

export default routes
