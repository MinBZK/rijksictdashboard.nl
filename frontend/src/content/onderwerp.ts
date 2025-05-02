import type { Onderwerp, OnderwerpenKey } from "@/types/content"

const onderwerpen: Record<OnderwerpenKey, Onderwerp> = {
  "Belastingen, uitkeringen en toeslagen": {
    urlRijksoverheid:
      "https://www.rijksoverheid.nl/onderwerpen/themas/belastingen-uitkeringen-en-toeslagen",
    img: "BelastingenToeslagenenUitkeringen.jpg",
    subonderwerpen: [
      {
        subonderwerp: "Belastingen",
        waarde:
          "Iedereen in Nederland maakt gebruik van voorzieningen waar de overheid voor zorgt of aan meebetaalt. Dit zijn bijvoorbeeld wegen en dijken, politie, onderwijs, zorg en sociale voorzieningen. Deze overheidstaken worden voor het grootste deel betaald uit de opbrengst van belastingen.",
      },
      {
        subonderwerp: "Uitkeringen en toeslagen",
        waarde:
          "Nederland is een welvarend land. Maar soms heeft iemand hulp nodig. Zo krijgen mensen zonder inkomen een uitkering. Daarnaast zijn er overheidsbijdragen in de kosten voor zorg, huur en kinderopvang. Ook zorgt de overheid voor subsidies aan ondernemers en woningbezitters.",
      },
    ],
  },
  "Recht, veiligheid en defensie": {
    img: "RechtVeiligheidDefensie.jpg",
    urlRijksoverheid:
      "https://www.rijksoverheid.nl/onderwerpen/themas/recht-veiligheid-en-defensie",
    subonderwerpen: [
      {
        subonderwerp: "Recht",
        waarde:
          "Het recht binnen Nederland is vastgelegd in regels en wetten. Dit voorkomt dat mensen het recht in eigen hand nemen. Of mensen worden benadeeld. Als dit het geval is, doet een rechter een rechterlijke uitspraak. De overheid zorgt ervoor dat deze uitspraken onafhankelijk zijn. Ook zorgt de overheid ervoor dat iedereen de rechtspraak kan inschakelen als dit nodig is. ",
      },
      {
        subonderwerp: "Veiligheid",
        waarde:
          "Het is belangrijk dat iedereen in Nederland zich veilig voelt. Belangrijk hierbij zijn een prettige leefomgeving en een goed werkende rechtstaat. Daarom bewaken politie en justitie de openbare orde en proberen ze criminaliteit te voorkomen. Ook zorgen ze ervoor dat de Nederlandse wetten en regels uitgevoerd kunnen worden. ",
      },
      {
        subonderwerp: "Defensie",
        waarde:
          "Defensie zet zich in voor vrede en veiligheid. Nederland draagt hierdoor bij aan de stabiliteit en vrijheid in de wereld. De marine, landmacht, luchtmacht en marechaussee kunnen overal ter wereld optreden. Bij internationale missies helpt de krijgsmacht ook mee aan de wederopbouw van een land.",
      },
    ],
  },
  "Bouwen en wonen": {
    urlRijksoverheid:
      "https://www.rijksoverheid.nl/onderwerpen/themas/bouwen-en-wonen",
    img: "BouwenEnWonen.jpg",
    subonderwerpen: [
      {
        subonderwerp: "",
        waarde:
          "Voor het kopen of huren van een woning bestaan allerlei regelingen. Voor het bouwen of verbouwen heeft u vaak een vergunning nodig. Daarnaast zijn er subsidiemogelijkheden om duurzaam te (ver-)bouwen.",
      },
    ],
  },
  Economie: {
    urlRijksoverheid:
      "https://www.rijksoverheid.nl/onderwerpen/themas/economie",
    img: "Economie.jpg",
    subonderwerpen: [
      {
        subonderwerp: "",
        waarde:
          "Het kabinet geeft ondernemers meer ruimte. Bijvoorbeeld door onnodige regels te schrappen. Dit helpt bedrijven om te blijven ondernemen. Daarnaast is er aandacht voor de leefomgeving. Zo blijft Nederland een goede plek om te werken, te wonen en te ondernemen.",
      },
    ],
  },
  "Familie, zorg en gezondheid": {
    urlRijksoverheid:
      "https://www.rijksoverheid.nl/onderwerpen/themas/familie-zorg-en-gezondheid",
    img: "FamilieEnZorg.jpg",
    subonderwerpen: [
      {
        subonderwerp: "Familie",
        waarde:
          "Kinderen en jongeren moeten kansen krijgen om zich goed te ontwikkelen. Zodat ze hun talenten kunnen ontplooien. Of plezier kunnen hebben. Zodra kinderen in de knel raken of de ouders hulp nodig hebben, is er zorg, bescherming en financiële steun.",
      },
      {
        subonderwerp: "Zorg en gezondheid",
        waarde:
          "Iedereen heeft recht op goede en veilige zorg. De overheid zet zich in voor een gezond Nederland. Daarbij staan kwaliteit en betaalbaarheid van de zorg voorop.",
      },
    ],
  },
  "Internationale samenwerking": {
    urlRijksoverheid:
      "https://www.rijksoverheid.nl/onderwerpen/themas/internationale-samenwerking",
    img: "InternationaleSamenwerking.jpg",
    subonderwerpen: [
      {
        subonderwerp: "",
        waarde:
          "Voor Nederland zijn goede Europese en internationale betrekkingen van groot belang. Ons land bouwt mee aan een veilige, stabiele en welvarende wereld.",
      },
    ],
  },
  "Klimaat, milieu en natuur": {
    img: "KimaatMilieuNatuur.jpg",
    urlRijksoverheid:
      "https://www.rijksoverheid.nl/onderwerpen/themas/klimaat-milieu-en-natuur",
    imgAuthor: "Jurrian Vlijm",
    subonderwerpen: [
      {
        subonderwerp: "Klimaat en milieu",
        waarde:
          "In Nederland wonen 16 miljoen mensen op een klein oppervlak. De overheid verdeelt deze ruimte tussen mens, dier en natuur. Ook de klimaatverandering speelt een rol bij die verdeling. Zo is er ruimte nodig om Nederland te beschermen tegen overstromingen.",
      },
      {
        subonderwerp: "Natuur",
        waarde:
          "Met respect voor mens, dier en omgeving zorgt de overheid voor gezond voedsel en een sterke agrarische economie. Voor waardevolle natuur. Voor een mooi landschap. De overheid werkt hiervoor samen met burgers, ondernemers en maatschappelijke organisaties.",
      },
    ],
  },
  "Migratie en reizen": {
    urlRijksoverheid:
      "https://www.rijksoverheid.nl/onderwerpen/themas/migratie-en-reizen",
    img: "Reizen.jpg",
    subonderwerpen: [
      {
        subonderwerp: "",
        waarde:
          "De overheid helpt Nederlanders die naar het buitenland gaan voor vakantie, wonen, werk of studie. Met informatie over landen, (reis-)adviezen en (reis-)tips kunt u zich voorbereiden op uw verblijf in het buitenland. Hierbij is ook aandacht voor de risico’s die daaraan verbonden zijn. ",
      },
      {
        subonderwerp: "",
        waarde:
          "De overheid voert ook het vreemdelingenbeleid uit. Elk verzoek om toelating wordt zorgvuldig afgewogen. Degene die een verblijfsvergunning krijgt, burgert in binnen de Nederlandse samenleving. Inburgeren is bijvoorbeeld het spreken van de Nederlandse taal en het hebben van kennis over de Nederlandse samenleving.",
      },
    ],
  },
  Onderwijs: {
    img: "Onderwijs.jpg",
    urlRijksoverheid:
      "https://www.rijksoverheid.nl/onderwerpen/themas/onderwijs",
    subonderwerpen: [
      {
        subonderwerp: "",
        waarde:
          "Toegankelijk en goed onderwijs is onmisbaar in onze maatschappij. Investeren in kennis is investeren in de toekomst. De overheid spant zich daarvoor in. Scholen krijgen daarbij zoveel mogelijk vrijheid. Via het wetenschapsbeleid stimuleert de overheid prestatie en vernieuwing.",
      },
    ],
  },
  "Overheid en democratie": {
    img: "Democratie.jpg",
    urlRijksoverheid:
      "https://www.rijksoverheid.nl/onderwerpen/themas/overheid-en-democratie",
    subonderwerpen: [
      {
        subonderwerp: "",
        waarde:
          "De overheid beschermt de belangen van alle burgers zo goed mogelijk. Ze maakt en bewaakt regels en wetten en helpt mensen waar dat nodig is. Het openbaar bestuur bestaat uit vier lagen: rijk, provincies, gemeenten en waterschappen.",
      },
    ],
  },
  "Verkeer en vervoer": {
    img: "VerkeerEnVervoer.jpg",
    urlRijksoverheid:
      "https://www.rijksoverheid.nl/onderwerpen/themas/verkeer-en-vervoer",
    imgAuthor: "IenM/Beter Benutten",
    subonderwerpen: [
      {
        subonderwerp: "",
        waarde:
          "Steeds meer mensen reizen met de auto en via het openbaar vervoer. Ook het goederenvervoer neemt toe. De overheid investeert in een beter wegennet en legt nieuwe spoorwegen aan. Zo kan iedereen vlot en veilig reizen.",
      },
    ],
  },
  Werk: {
    img: "Werk.jpg",
    urlRijksoverheid: "https://www.rijksoverheid.nl/onderwerpen/themas/werk",
    subonderwerpen: [
      {
        subonderwerp: "",
        waarde:
          "Werken aan de eigen loopbaan en blijven leren. Als betaald werken nog niet kan, helpt de overheid om dit te bereiken. De overheid werkt aan een sociaal en economisch sterk Nederland met werk en bestaanszekerheid voor iedereen.",
      },
    ],
  },
}

export default onderwerpen
