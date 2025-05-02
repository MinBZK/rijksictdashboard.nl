<template>
  <TextLoaderContent
    content-group="Informatiehuishouding"
    content-field-key="content"
  />
  <TextLoaderContent
    v-for="key in expandableContentKeys"
    :key="key"
    content-group="Informatiehuishouding"
    :content-field-key="key"
    :title="key"
    :expandable="true"
  />
  <ExpandContent title="Huidige stand van zaken">
    <GrafiekGemiddeldVolwassenheidsniveau />
    <TextLoaderContent
      content-group="Informatiehuishouding"
      content-field-key="Huidige stand van zaken"
    />
  </ExpandContent>

  <ExpandContent title="Stand van zaken per thema">
    <RidRow>
      <v-col v-for="g in gaugeCharts" :key="g.title" :lg="3" :cols="6">
        <figcaption class="text-subtitle-1">{{ g.title }}</figcaption>
        <img
          :src="g.img"
          :alt="`Score op een schaal van 1 tot 5: ${g.value}`"
        />
      </v-col>
    </RidRow>
    <TextLoaderContent
      content-group="Informatiehuishouding"
      content-field-key="Stand van zaken per thema"
    />
  </ExpandContent>
</template>

<script setup lang="ts">
import TextLoaderContent from "@/components/TextLoaderContent.vue"
import GrafiekGemiddeldVolwassenheidsniveau from "@/views/Informatiehuishouding/GrafiekGemiddeldVolwassenheidsniveau.vue"
import RidRow from "@/components/RidRow.vue"
import ExpandContent from "@/components/ExpandContent.vue"

const expandableContentKeys = [
  "Verbeteren van de informatiehuishouding",
  "Volwassenheidsmeting",
]

type GaugeChart = {
  img: string
  title: string
  value: string
}

const gaugeCharts: GaugeChart[] = [
  {
    img: "/img/informatiehuishouding/gauge-professionals.png",
    title: "Professionals",
    value: "2,2",
  },
  {
    img: "/img/informatiehuishouding/gauge-volume-en-aard-van-informatie.png",
    title: "Volume en aard van informatie",
    value: "1,9",
  },
  {
    img: "/img/informatiehuishouding/gauge-informatiesystemen.png",
    title: "Informatiesystemen",
    value: "2,3",
  },
  {
    img: "/img/informatiehuishouding/gauge-bestuur-en-naleving.png",
    title: "Bestuur en naleving",
    value: "2,5",
  },
]
</script>
