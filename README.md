# Over het Rijks ICT-dashboard

Het Rijks ICT-dashboard biedt inzicht in grootschalige ICT-projecten van de Rijksoverheid. Het is ontwikkeld met een focus op transparantie en toegankelijkheid. Het ontwikkelteam werkt met een open ontwikkelaanpak en maakt gebruik van open source software, zodat iedereen kan meekijken en bijdragen.

Je kunt de voortgang van het project en de broncode bekijken op GitHub. Het dashboard is voortdurend in ontwikkeling. Nieuwe projecten worden toegevoegd en bestaande informatie wordt regelmatig bijgewerkt.

Het Rijks ICT-dashboard wordt ontwikkeld met open source software. De broncode is vrij beschikbaar op GitHub. Deze kan bekeken, gedownload en hergebruikt worden. GitHub biedt transparante versiebeheerfuncties, waardoor samenwerking en het volgen van wijzigingen tijdens de ontwikkeling eenvoudig is.

## Motivatie

De overheid voert veel grote en complexe ICT-projecten uit die essentieel zijn voor publieke dienstverlening en de samenleving. Om transparantie, verantwoording en publiek vertrouwen te waarborgen, is het belangrijk dat iedereen kan zien hoe deze projecten vorderen.

Het Rijks ICT-dashboard maakt informatie over deze ICT-projecten van de overheid toegankelijk voor iedereen: burgers, journalisten, onderzoekers, beleidsmakers en andere belanghebbenden. Het ondersteunt open overheid door inzicht te geven in tijdslijnen, budgetten en projectdoelen, zodat iedereen geïnformeerd en betrokken kan blijven.

### Open source software

Doe je mee en deel je mening? Om bij te dragen maak je een account aan op GitHub (https://github.com/signup) en lees je deze readme en de gedragscode om aan de slag te gaan.

Eenmaal aangemeld kun je feedback geven op de code of de gebruiksvriendelijkheid van de website. Begin vandaag nog: doe mee en deel je mening!

# Technische informatie

Voor het lokaal draaien van de applicatie zijn de volgende tools vereist:

- Docker ([installatie-instructies](https://docs.docker.com/get-docker/))
- Node.js. De versie staat vermeld in `frontend/.nvmrc`. Het is aanbevolen om [Node version manager](https://github.com/nvm-sh/nvm) te gebruiken; met `nvm use` kun je dan de juiste versie activeren.
- Python. De versie staat vermeld in `backend/.python-version`. Gebruik bij voorkeur [pyenv](https://github.com/pyenv/pyenv) om tussen versies te wisselen, maar dit is niet verplicht.
- Poetry. Zie de [documentatie](https://python-poetry.org/docs/#installation) voor installatie-instructies.
- Make. Dit is een build-automatiseringstool. Deze is doorgaans al geïnstalleerd op Linux en macOS. Voor Windows kun je Make installeren via [Chocolatey](https://chocolatey.org/) of [Git for Windows](https://gitforwindows.org/).

De documentatie is getest op Ubuntu, maar zou ook op Windows moeten werken.

### Omgevingsvariabelen

Omgevingsvariabelen worden opgeslagen in `.env` in de map `backend`, maar omdat deze geheimen kunnen bevatten (zoals wachtwoorden), zijn ze niet opgenomen in de repository. Kopieer daarom `.env.dummy` naar `.env` in dezelfde map.

### Database

1. Start de database. Voer in de map `/backend` het volgende commando uit: `make init_db`.

Controleer of de database draait via de GUI (DBgate) op `http://localhost:8091/`. Daar zou je de database `rid-data` moeten kunnen openen.

### De applicatie lokaal draaien

### Backend

Alle onderstaande commando’s voer je uit vanuit de map `/backend`.

1. Specificeer de Python-versie voor de virtuele omgeving: `poetry env use <python_versie>`. (De vereiste versie staat in `backend/.python-version`.)
2. Installeer de pakketten: `poetry install`.
3. Activeer de virtuele omgeving: `poetry shell`.
4. Start de backend: `make server`

Controleer of de backend draait door te navigeren naar de documentatie op `http://localhost:8000/api-docs`.

### Frontend

1.  Installeer afhankelijkheden. Voer in de map `/frontend` uit: `npm install`.
2.  Start de lokale server. Voer in de map `/frontend` uit: `npm run dev -- --port 5473`.

Controleer of de frontend draait door te navigeren naar `http://localhost:5473`.

### De applicatie draaien met Docker

Je kunt het volledige project ook draaien met Docker vanuit de root-map. Dit is de makkelijkste manier om alles werkend te krijgen zonder handmatig alle afhankelijkheden te installeren.

Voer in de root van het project het volgende commando uit om alle services te starten: `make init_app`.

Controleer of de applicatie draait via:
Backend: `http://localhost:8000/api-docs`
Frontend: `http://localhost:5473`
