<template>
  <page title="Kwetsbaarheid melden" :text-only="true">
    <div>
      <TextLoaderContent
        content-group="Kwetsbaarheid melden"
        content-field-key="content"
      />
      <a
        href="https://www.ncsc.nl/contact/kwetsbaarheid-melden"
        class="mt-5 no-icon"
        target="_blank"
        rel="noopener"
      >
        <RidButton prepend-icon="mdi-alert-octagram" type="submit"
          >Meld een kwetsbaarheid</RidButton
        >
      </a>
    </div>
  </page>
</template>

<script setup lang="ts">
import Page from "@/components/Page.vue"
import RidButton from "@/components/RidButton.vue"
import TextLoaderContent from "@/components/TextLoaderContent.vue"
</script>
