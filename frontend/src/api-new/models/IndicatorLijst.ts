/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Formulier } from './Formulier';
import type { IndicatorlijstNamen } from './IndicatorlijstNamen';
export type IndicatorLijst = {
    IndicatorLijstId: string;
    IndicatorLijstMeervoudsNaam: IndicatorlijstNamen;
    IndicatorLijstEnkelFormulier: boolean;
    IndicatorLijstIndex: number;
    Formulier: Array<Formulier>;
    FormulierDict?: null;
    DatumIndexVeld: (string | null);
};

