import type { Ref } from "vue"
import type { ProjectMetAlleMetricsEnIndicatorLijsten } from "@/api-new"
import type { IndicatorLijstMetBerekendeAttributen } from "@/types/indicatorlijst"
import type { IndicatorlijstNamen } from "@/api-new"

const indicatorlijstNaamMapping: { [K in IndicatorlijstNamen]?: string } = {
  "Maatschappelijke baten": "Meerwaarde per doelgroep",
}

export type IndicatorLijstMetAlias = IndicatorLijstMetBerekendeAttributen & {
  IndicatorLijstMeervoudsNaamAlias: string
}

export const useIndicatorLijst = (
  project: Ref<ProjectMetAlleMetricsEnIndicatorLijsten | null>,
) => {
  const getIndicatorLijst = (lijstNaam: IndicatorlijstNamen) => {
    if (project.value) {
      const lijst = project.value.IndicatorLijstWaardesGecorrigeerd.find(
        (pA) => pA.IndicatorLijstMeervoudsNaam == lijstNaam,
      )
      if (lijst) {
        const lijstBerekend: IndicatorLijstMetBerekendeAttributen = {
          ...lijst,
          // filter lege rijen eruit
          FormulierGefilterd:
            lijst?.Formulier.filter(
              (f) =>
                f.FormulierWaardes.filter(
                  (fW) => (fW.Waarde || "").toString().length > 0,
                ).length > 0,
            ) || [],
        }

        const lijstBerekendMetAlias: IndicatorLijstMetAlias = {
          ...lijstBerekend,
          ...{
            IndicatorLijstMeervoudsNaamAlias:
              indicatorlijstNaamMapping[
                lijstBerekend.IndicatorLijstMeervoudsNaam
              ] || lijstBerekend.IndicatorLijstMeervoudsNaam,
          },
        }

        return lijstBerekendMetAlias
      } else {
        return undefined
      }
    }
  }

  return { getIndicatorLijst }
}
