/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $IndicatorLijst = {
    properties: {
        IndicatorLijstId: {
            type: 'string',
            isRequired: true,
        },
        IndicatorLijstMeervoudsNaam: {
            type: 'IndicatorlijstNamen',
            isRequired: true,
        },
        IndicatorLijstEnkelFormulier: {
            type: 'boolean',
            isRequired: true,
        },
        IndicatorLijstIndex: {
            type: 'number',
            isRequired: true,
        },
        Formulier: {
            type: 'array',
            contains: {
                type: 'Formulier',
            },
            isRequired: true,
        },
        FormulierDict: {
            type: 'any-of',
            contains: [{
                type: 'null',
            }],
        },
        DatumIndexVeld: {
            type: 'any-of',
            contains: [{
                type: 'string',
            }, {
                type: 'null',
            }],
            isRequired: true,
        },
    },
} as const;
