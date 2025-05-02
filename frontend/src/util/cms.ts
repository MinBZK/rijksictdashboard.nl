import type { Formulier } from "@/api-new"

type FormulierDict = {
  [key: string]: FormulierWaardeDict
}

type FormulierWaardeDict = {
  value: string | undefined
  type: string
}

const getFormulierAsDict = (formulier: Formulier) => {
  const formulierWaardes = formulier.FormulierWaardes
  return formulierWaardes.reduce((obj, indicatorWaarde) => {
    obj[indicatorWaarde.IndicatorTitel] = {
      value: indicatorWaarde.Waarde || undefined,
      type: indicatorWaarde.IndicatorAntwoordTypeNaam,
    }
    return obj
  }, {} as FormulierDict)
}

export { getFormulierAsDict }
