/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $FormulierWaarde = {
    properties: {
        IndicatorTitel: {
            type: 'string',
            isRequired: true,
        },
        IndicatorIndex: {
            type: 'number',
            isRequired: true,
        },
        IndicatorAntwoordTypeNaam: {
            type: 'string',
            isRequired: true,
        },
        Waarde: {
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
