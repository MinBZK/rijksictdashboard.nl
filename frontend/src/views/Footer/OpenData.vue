<template>
  <TextLoaderContent content-group="Open data" content-field-key="content" />

  <RidRow class="mt-8">
    <RidCol :lg="2" :sm="6" :has-border="false" :no-padding="true">
      <Dropdown
        v-model="selectedFileType"
        :items="
          items.map((y) => {
            return { title: y, value: y }
          })
        "
        label="Selecteer bestandsformaat"
      />
    </RidCol>
    <RidCol :lg="2" :sm="6" :has-border="false" :no-padding="true">
      <div class="buttons mb-3">
        <form
          :action="links[selectedFileType]"
          :target="selectedFileType === DataFormat.JSON ? '_blank' : ''"
        >
          <RidButton
            variant="tonal"
            prepend-icon="mdi-download"
            type="submit"
            class="custom-width-button custom-taller-button mt-4 ml-2 text-none"
            >Download</RidButton
          >
        </form>
      </div>
    </RidCol>
  </RidRow>
</template>

<script setup lang="ts">
import RidButton from "@/components/RidButton.vue"
import { jsonUrl, spreadsheetUrl } from "@/services/project"
import TextLoaderContent from "@/components/TextLoaderContent.vue"
import RidRow from "@/components/RidRow.vue"
import RidCol from "@/components/RidCol.vue"
import Dropdown from "@/components/Dropdown.vue"

enum DataFormat {
  Excel = "Excel-formaat",
  ODS = "ODS-formaat",
  JSON = "JSON-formaat",
}

const items: DataFormat[] = Object.values(DataFormat)

const links: Record<DataFormat, string> = {
  [DataFormat.Excel]: spreadsheetUrl("excel"),
  [DataFormat.ODS]: spreadsheetUrl("ods"),
  [DataFormat.JSON]: jsonUrl,
}

const selectedFileType = ref<DataFormat>(DataFormat.Excel)
</script>

<style scoped lang="scss">
:deep(.v-btn__content) {
  letter-spacing: normal;
  font-size: 1.2em;
}
.custom-width-button {
  width: 100%;
}
.custom-taller-button {
  height: 53px;
}
.buttons {
  display: flex;
}
</style>
