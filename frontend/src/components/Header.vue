<template>
  <header id="header">
    <div id="mainwrapper" class="logo-wrapper ma-0 pa-0">
      <figure>
        <img
          alt="Rijksoverheid Logo"
          src="../assets/logo-ro-zonder-caption.svg"
          class="logo-full"
        />
        <img
          alt="Rijksoverheid Logo"
          src="../assets/logo-ro-zonder-caption-mobile.svg"
          class="logo-mobile"
        />
        <figcaption class="logo-caption">Rijksoverheid</figcaption>
      </figure>
    </div>
  </header>

  <div id="bar" class="bar-wrapper">
    <div class="bar-wrapper-content pl-5">
      <nav>
        <div class="text-left">
          <router-link :to="{ name: 'home' }">{{ title }}</router-link>
        </div>
        <div class="text-right">
          <button
            class="hamburger"
            aria-label="Toon het navigatiemenu"
            :aria-expanded="showNav ? 'true' : 'false'"
            @click="showNav = !showNav"
          >
            <v-icon>mdi-menu</v-icon>
          </button>
          <ul>
            <li v-for="p in pages" :key="p.routeName">
              <router-link
                :to="{ name: p.routeName }"
                :aria-current="route.name == p.routeName ? 'page' : undefined"
                >{{ p.label }}</router-link
              >
            </li>
          </ul>
        </div>
      </nav>
    </div>
    <div
      class="bar-wrapper-content nav-responsive pl-5"
      :class="{ hide: !showNav }"
    >
      <ul>
        <li v-for="p in pages" :key="p.routeName">
          <router-link
            :to="{ name: p.routeName }"
            :aria-current="route.name == p.routeName ? 'page' : undefined"
            >{{ p.label }}</router-link
          >
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title?: string
}>()

type HeaderItem = {
  routeName: string
  label: string
}

const pages: HeaderItem[] = [
  { routeName: "i-strategie", label: "I-strategie" },
  { routeName: "ICT-activiteiten", label: "Grote ICT-activiteiten" },
  { routeName: "ministeries", label: "Ministeries" },
  { routeName: "onderwerpen", label: "Onderwerpen" },
]

const showNav = ref<Boolean>(false)

const route = useRoute()
</script>

<style scoped lang="scss">
@import "@/styles/main.scss";

.logo-wrapper figure {
  display: flex;
  align-items: flex-start;
}

.logo {
  height: 76px;
}

.logo-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
  height: 70px;
}

.logo-wrapper img {
  margin-left: 90px;
  height: 70px;
}

.bar-wrapper {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  background-color: $primary;
  min-height: 76px;
}
.bar-wrapper nav,
.bar-wrapper div {
  padding: 0 8px 0 0;
}

.bar-wrapper-content {
  display: flex;
  flex-basis: 100%;
  flex-wrap: wrap;
  max-width: 1200px;
  flex-shrink: 0;
  align-items: center;
  justify-content: space-between;
  -webkit-margin-end: -16px;
  margin-inline-end: -16px;
  -webkit-margin-start: -16px;
  margin-inline-start: -16px;
  position: relative;
  min-height: 76px;
}

.bar-wrapper-content div a,
.bar-wrapper-content nav {
  color: white;
}

.logo-caption {
  font-family:
    RO Serif,
    Calibri,
    sans-serif;
  font-size: 1rem;
  line-height: 1.1;
  width: 100%;
  max-width: 300px;
  padding: 20px 10px 10px;
  color: #000;
}

nav {
  display: flex;
  justify-content: space-between;
  width: 100%;

  :hover {
    text-decoration: underline;
  }
}

nav ul {
  display: none;
}

nav ul > li {
  font-size: 24px;
  display: block;
  padding: 0 0 0 1em;
}

.barwapper ul > li a {
  color: white;
  text-decoration: none;
  display: block;
}

.hide {
  display: none;
}

.nav-responsive a {
  color: white !important;
  font-size: 14pt;
}

.nav-responsive li {
  padding: 0.5em 0;
  list-style-type: none;
}

.bar-wrapper-content nav a {
  color: white;
  text-decoration: none;
}

.hamburger {
  cursor: pointer;
  display: flex;
  font-size: 18pt;
}

@media (min-width: 768px) {
  nav ul > li {
    display: inline-block;
  }

  .nav-responsive {
    display: none;
  }

  nav ul {
    list-style: none;
    display: table;
    vertical-align: middle;
  }

  .hamburger {
    display: none;
  }
  .logo-caption {
    padding: 50px 12px 25px;
  }

  .logo-wrapper {
    height: 125px;
  }

  .logo-wrapper img {
    height: 125px;
    margin-left: 112px;
  }

  img.logo-full {
    display: block;
  }

  img.logo-mobile {
    display: none;
  }
}

.logo-mobile {
  display: block;
}

.logo-full {
  display: none;
}

.bar-wrapper-content div a {
  font-size: 24px;
}
</style>
