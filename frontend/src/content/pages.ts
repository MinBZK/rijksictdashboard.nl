import type { RouteRecordName } from "vue-router"

type PageGroupName = "I-strategie" | "Grote ICT-activiteiten" | "Overig"

type PageBlockImage = {
  imgUrl: string
  imgAuthor?: string
}

type PageGroup = {
  name: PageGroupName
  description: TextLoaderField
  image: PageBlockImage
  mainPage: RidPage
}

type TextLoaderField = {
  contentName: string
  contentKey: string
}

export type RidPage = {
  title: string
  longTitle?: string
  previewText: TextLoaderField
  routeName: string
  alternativeEntryRouteNames?: RouteRecordName[]
  image: PageBlockImage
  author?: string
  groupName?: PageGroupName
  // specify an alternative context for the page. This means the page will first appear in the group specified in 'groupName',
  // but on the page itself, pages within the group 'contextGroup' will be diplsayed
  contextGroupName?: PageGroupName
}

const pages: RidPage[] = [
  {
    title: "Wat we verbeteren",
    routeName: "wat we verbeteren",
    previewText: {
      contentKey: "Home",
      contentName: "MaatschappelijkeBaten",
    },
    image: {
      imgUrl: "/img/home/maatschappelijke-baten2.jpg",
    },
    groupName: "Overig",
  },
  {
    title: "Wat we verbeteren",
    previewText: {
      contentKey: "Maatschappelijke baten",
      contentName: "preview",
    },
    routeName: "wat we verbeteren",
    alternativeEntryRouteNames: ["wat we verbeteren detail"],
    image: {
      imgUrl: "/img/home/maatschappelijke-baten.png",
      imgAuthor: "Inge van Mil Photography",
    },
  },
  {
    title: "ICT-kosten",
    previewText: {
      contentKey: "Home",
      contentName: "IctKosten",
    },
    routeName: "ICT-kosten",
    image: {
      imgUrl: "/img/home/ict-kosten.png",
    },
    groupName: "Overig",
  },
  {
    title: "Duurzaamheid",
    previewText: {
      contentKey: "Duurzaamheid",
      contentName: "preview",
    },
    routeName: "duurzaamheid",
    image: {
      imgUrl: "/img/home/duurzaamheid.jpg",
    },
    groupName: "Overig",
  },
  {
    title: "Overzicht van grote ICT-activiteiten",
    routeName: "ICT-activiteiten",
    previewText: {
      contentKey: "Grote ICT-activiteiten",
      contentName: "preview",
    },
    image: {
      imgUrl: "/img/home/grote-ict-activiteiten.jpg",
      imgAuthor: "Ruud Sies (SiesvanHintum Rotterdam)",
    },
    groupName: "Grote ICT-activiteiten",
  },
  {
    title: "ICT-activiteiten per onderwerp",
    routeName: "onderwerpen",
    previewText: {
      contentKey: "Onderwerpen",
      contentName: "preview",
    },
    image: {
      imgUrl: "/img/home/ict-activiteiten-per-onderwerp.jpg",
    },
    groupName: "Grote ICT-activiteiten",
  },
  {
    title: "Open data",
    routeName: "Open data",
    previewText: {
      contentKey: "Home",
      contentName: "OpenData",
    },
    image: {
      imgUrl: "/img/home/open-data.jpg",
    },
    groupName: "Grote ICT-activiteiten",
  },
  {
    title: "ICT-medewerkers",
    longTitle: "ICT-medewerkers (thema 7)",
    routeName: "ICT-medewerkers",
    previewText: {
      contentKey: "ICT-medewerkers",
      contentName: "preview",
    },
    image: {
      imgUrl: "/img/home/ict-medewerkers.jpg",
    },
    groupName: "I-strategie",
  },
  // {
  //   title: "Toegankelijkheid",
  //   routeName: "Toegankelijkheid",
  //   previewText: {
  //     contentKey: "Toegankelijkheid",
  //     contentName: "preview",
  //   },
  //   image: {
  //     imgUrl: "/img/home/toegankelijkheid.jpg",
  //   },
  //   groupName: "Overig",
  // },
  // {
  //   title: "Artificiële intelligentie",
  //   longTitle: "Artificiële intelligentie (thema 6)",
  //   routeName: "AI",
  //   previewText: {
  //     contentKey: "AI",
  //     contentName: "preview",
  //   },
  //   imgUrl: "/img/home/artifical-intelligence.jpg",
  //   groupName: "I-strategie",
  // },
  {
    title: "Algoritmes en AI",
    longTitle: "Algoritmes en AI (thema 6)",
    routeName: "Algoritmes en AI",
    previewText: {
      contentKey: "Algoritmen",
      contentName: "preview",
    },
    image: {
      imgUrl: "/img/home/algoritmes.jpg",
    },
    groupName: "I-strategie",
  },
  {
    title: "Informatiehuishouding",
    longTitle: "Informatiehuishouding (thema 5)",
    routeName: "Informatiehuishouding",
    previewText: {
      contentKey: "Informatiehuishouding",
      contentName: "preview",
    },
    image: {
      imgUrl: "/img/home/informatiehuishouding.jpg",
      imgAuthor: "Wiebe Kiestra Fotografie",
    },
    groupName: "I-strategie",
  },
  {
    title: "Architectuur",
    longTitle: "Architectuur (thema 3)",
    routeName: "Architectuur",
    previewText: {
      contentKey: "Architectuur",
      contentName: "preview",
    },
    image: {
      imgUrl: "/img/home/architectuur.jpg",
    },
    groupName: "I-strategie",
  },
  {
    title: "IT-Assetmanagement",
    longTitle: "IT-Assetmanagement (thema 3)",
    routeName: "IT-Assetmanagement",
    previewText: {
      contentKey: "Softwarekwaliteit",
      contentName: "preview",
    },
    image: {
      imgUrl: "/img/home/softwarekwaliteit.png",
    },
    groupName: "I-strategie",
  },

  {
    title: "Grote ICT-activiteiten",
    longTitle: "Grote ICT-activiteiten (thema 8)",
    routeName: "Dashboard",
    previewText: {
      contentKey: "Grote ICT-activiteiten",
      contentName: "preview",
    },
    image: {
      imgUrl: "/img/home/grote-ict-activiteiten.jpg",
      imgAuthor: "Ruud Sies (SiesvanHintum Rotterdam)",
    },
    groupName: "I-strategie",
    contextGroupName: "Grote ICT-activiteiten",
  },

  {
    title: "Informatiebeveiliging",
    longTitle: "Informatiebeveiliging (thema 2)",
    routeName: "Informatiebeveiliging",
    previewText: {
      contentKey: "Informatiebeveiliging",
      contentName: "preview",
    },
    image: {
      imgUrl: "/img/home/informatiebeveiliging.jpg",
    },
    groupName: "I-strategie",
  },
]

const pageGroups: PageGroup[] = [
  {
    name: "I-strategie",
    image: {
      imgUrl: "/img/home/i-strategie.jpg",
      imgAuthor: "Herman Zonderland Fotografie Delft",
    },
    description: {
      contentKey: "I-strategie",
      contentName: "preview",
    },
    mainPage: {
      title: "I-strategie",
      previewText: {
        contentKey: "I-strategie",
        contentName: "preview",
      },
      routeName: "i-strategie",
      image: {
        imgUrl: "/img/home/i-strategie.jpg",
        imgAuthor: "Herman Zonderland Fotografie Delft",
      },
      groupName: "I-strategie",
    },
  },
  {
    name: "Grote ICT-activiteiten",
    image: {
      imgUrl: "/img/home/grote-ict-activiteiten.jpg",
      imgAuthor: "Ruud Sies (SiesvanHintum Rotterdam)",
    },
    description: {
      contentKey: "Grote ICT-activiteiten",
      contentName: "preview",
    },
    mainPage: {
      title: "Inzicht in grote ICT-activiteiten",
      routeName: "Dashboard",
      previewText: {
        contentKey: "ICT-medewerkers",
        contentName: "preview",
      },
      image: {
        imgUrl: "img/home/dashboard.png",
      },
      groupName: "Grote ICT-activiteiten",
    },
  },
]

export { pages, pageGroups }
