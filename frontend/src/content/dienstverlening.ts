// this data can be updated by running the scraping notebook in backend/notebooks
const urls: Record<string, string> = {
  "Aanpak belastingontwijking en belastingontduiking":
    "/onderwerpen/aanpak-belastingontwijking-en-belastingontduiking",
  "Algemene nabestaandenwet (Anw)": "/onderwerpen/algemene-nabestaandenwet-anw",
  AOW: "/onderwerpen/algemene-ouderdomswet-aow",
  "Arbeidsongeschikt na ziekte (WIA)": "/onderwerpen/wia",
  Armoedebestrijding: "/onderwerpen/armoedebestrijding",
  "Belasting betalen": "/onderwerpen/belasting-betalen",
  "Belasting op auto en motor": "/onderwerpen/belastingen-op-auto-en-motor",
  "Belastingen voor ondernemers": "/onderwerpen/belastingen-voor-ondernemers",
  Belastingverdragen: "/onderwerpen/belastingverdragen",
  Bijstand: "/onderwerpen/bijstand",
  "Aardgasvrije wijken": "/onderwerpen/aardgasvrije-wijken",
  Asbest: "/onderwerpen/asbest",
  Bevolkingsdaling: "/onderwerpen/bevolkingsdaling",
  Bouwproducten: "/onderwerpen/bouwproducten",
  Bouwregelgeving: "/onderwerpen/bouwregelgeving",
  "Duurzaam bouwen en verbouwen": "/onderwerpen/duurzaam-bouwen-en-verbouwen",
  "Eigen huis bouwen": "/onderwerpen/eigen-huis-bouwen",
  "Energie thuis": "/onderwerpen/energie-thuis",
  "Energielabel woningen en gebouwen":
    "/onderwerpen/energielabel-woningen-en-gebouwen",
  "Gezond en veilig wonen": "/onderwerpen/gezond-en-veilig-wonen",
  Aanbesteden: "/onderwerpen/aanbesteden",
  "Afhandeling schade wateroverlast Limburg en Noord-Brabant":
    "/onderwerpen/afhandeling-schade-wateroverlast-limburg-en-noord-brabant",
  "Bescherming van consumenten": "/onderwerpen/bescherming-van-consumenten",
  Biotechnologie: "/onderwerpen/biotechnologie",
  Brexit: "/onderwerpen/brexit",
  "Certificaten, normen en meetinstrumenten":
    "/onderwerpen/certificaten-keurmerken-en-meetinstrumenten",
  "Circulaire economie": "/onderwerpen/circulaire-economie",
  "Commissariaat Militaire Productie (CMP)":
    "/onderwerpen/commissariaat-militaire-productie",
  "18 jaar worden": "/onderwerpen/achttien-jaar-worden",
  "Aangifte geboorte en naamskeuze kind":
    "/onderwerpen/aangifte-geboorte-en-naamskeuze-kind",
  Abortus: "/onderwerpen/abortus",
  Adoptie: "/onderwerpen/adoptie",
  Alcohol: "/onderwerpen/alcohol",
  Antibioticaresistentie: "/onderwerpen/antibioticaresistentie",
  "Beschermd wonen en maatschappelijke opvang":
    "/onderwerpen/beschermd-wonen-en-maatschappelijke-opvang",
  "Chroom-6 en CARC": "/onderwerpen/chroomverf",
  "Coronavirus COVID-19": "/onderwerpen/coronavirus-covid-19",
  Afghanistan: "/onderwerpen/afghanistan",
  "Associatieakkoord Oekra\u00efne": "/onderwerpen/associatieakkoord-oekraine",
  "Europese subsidies": "/onderwerpen/europese-subsidies",
  "Europese Unie": "/onderwerpen/europese-unie",
  "Financi\u00ebn Europese Unie": "/onderwerpen/financien-europese-unie",
  "Geestelijke gezondheidszorg en psychosociale steun bij noodhulp":
    "/onderwerpen/geestelijke-gezondheidszorg-en-psychosociale-steun-in-noodhulp",
  Handelsverdragen: "/onderwerpen/handelsverdragen-europese-unie",
  "Internationaal maatschappelijk verantwoord ondernemen (IMVO)":
    "/onderwerpen/internationaal-maatschappelijk-verantwoord-ondernemen-imvo",
  Afval: "/onderwerpen/afval",
  Bestrijdingsmiddelen: "/onderwerpen/bestrijdingsmiddelen",
  "Bodem en ondergrond": "/onderwerpen/bodem-en-ondergrond",
  Dierenwelzijn: "/onderwerpen/dierenwelzijn",
  Diergezondheid: "/onderwerpen/diergezondheid",
  Dierproeven: "/onderwerpen/dierproeven",
  Drinkwater: "/onderwerpen/drinkwater",
  "Droogte en hitte": "/onderwerpen/droogte-en-hitte",
  "Ambassades, consulaten en overige vertegenwoordigingen":
    "/onderwerpen/ambassades-consulaten-en-overige-vertegenwoordigingen",
  Asielbeleid: "/onderwerpen/asielbeleid",
  "Buitenlandse werknemers": "/onderwerpen/buitenlandse-werknemers",
  "Discriminatie en racisme": "/onderwerpen/discriminatie-en-racisme",
  "Eergerelateerd geweld": "/onderwerpen/eergerelateerd-geweld",
  "Immigratie naar Nederland": "/onderwerpen/immigratie-naar-nederland",
  "Inburgeren in Nederland": "/onderwerpen/inburgeren-in-nederland",
  "Internationale sociale zekerheid":
    "/onderwerpen/internationale-sociale-zekerheid",
  Migratie: "/onderwerpen/migratie",
  "Nederlandse nationaliteit": "/onderwerpen/nederlandse-nationaliteit",
  Basisonderwijs: "/onderwerpen/basisonderwijs",
  "Eindexamens voortgezet onderwijs": "/onderwerpen/eindexamens",
  "Financiering onderwijs": "/onderwerpen/financiering-onderwijs",
  "Gemengde scholen": "/onderwerpen/gemengde-scholen",
  "Hoger onderwijs": "/onderwerpen/hoger-onderwijs",
  Laaggeletterdheid: "/onderwerpen/laaggeletterdheid",
  Leerlingendaling: "/onderwerpen/leerlingendaling",
  Leerplicht: "/onderwerpen/leerplicht",
  "Leven Lang Ontwikkelen": "/onderwerpen/leven-lang-ontwikkelen",
  "Middelbaar beroepsonderwijs (mbo)":
    "/onderwerpen/middelbaar-beroepsonderwijs",
  Archieven: "/onderwerpen/archieven",
  "Beloningen bestuurders": "/onderwerpen/beloningen-bestuurders",
  "Bezwaar en beroep": "/onderwerpen/bezwaar-en-beroep",
  Burgerschap: "/onderwerpen/burgerschap",
  Campagnes: "/onderwerpen/campagnes",
  "Caribisch deel van het Koninkrijk":
    "/onderwerpen/caribische-deel-van-het-koninkrijk",
  Consignatiekas: "/onderwerpen/consignatiekas",
  "Coronavirus tijdlijn": "/onderwerpen/coronavirus-tijdlijn",
  Democratie: "/onderwerpen/democratie",
  "Aanpak seksueel grensoverschrijdend gedrag en seksueel geweld":
    "/onderwerpen/aanpak-seksueel-grensoverschrijdend-gedrag-en-seksueel-geweld",
  "Agressie en geweld in de samenleving":
    "/onderwerpen/agressie-en-geweld-in-de-samenleving",
  "Alarmnummer 112": "/onderwerpen/alarmnummer-112",
  "Bevoegdheden inlichtingendiensten en veiligheidsdiensten":
    "/onderwerpen/bevoegdheden-inlichtingendiensten-en-veiligheidsdiensten",
  "Communicatie door hulpdiensten via C2000":
    "/onderwerpen/communicatie-hulpdiensten-c2000",
  "Cybercrime en cybersecurity": "/onderwerpen/cybercrime-en-cybersecurity",
  Defensiematerieel: "/onderwerpen/defensiematerieel",
  Auto: "/onderwerpen/auto",
  Drone: "/onderwerpen/drone",
  Fiets: "/onderwerpen/fiets",
  Geluidsoverlast: "/onderwerpen/geluidsoverlast",
  Goederenvervoer: "/onderwerpen/goederenvervoer",
  Luchtvaart: "/onderwerpen/luchtvaart",
  "Milieuvriendelijke brandstoffen voor vervoer":
    "/onderwerpen/milieuvriendelijke-brandstoffen-voor-vervoer",
  "Mobiliteit nu en in de toekomst":
    "/onderwerpen/mobiliteit-nu-en-in-de-toekomst",
  "Openbaar vervoer (ov)": "/onderwerpen/openbaar-vervoer",
  Rijbewijs: "/onderwerpen/rijbewijs",
  "Aanpak schijnconstructies": "/onderwerpen/aanpak-schijnconstructies",
  "Adoptieverlof en pleegzorgverlof":
    "/onderwerpen/adoptieverlof-en-pleegzorgverlof",
  Arbeidsomstandigheden: "/onderwerpen/arbeidsomstandigheden",
  "Arbeidsovereenkomst en cao": "/onderwerpen/arbeidsovereenkomst-en-cao",
  "Bijbaan, vakantiewerk en stage door jongeren":
    "/onderwerpen/bijbaan-vakantiewerk-en-stage-door-jongeren",
  "Bijstand voor zelfstandigen (Bbz)":
    "/onderwerpen/bijstand-voor-zelfstandigen-bbz",
  "Calamiteitenverlof en kort verzuimverlof": "/onderwerpen/calamiteitenverlof",
  "Dienstverlening aan huis": "/onderwerpen/dienstverlening-aan-huis",
}

export default urls
