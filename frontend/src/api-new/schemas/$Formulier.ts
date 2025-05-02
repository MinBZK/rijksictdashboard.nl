/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $Formulier = {
    properties: {
        FormulierId: {
            type: 'string',
            isRequired: true,
        },
        FormulierAanmaakDatum: {
            type: 'string',
            isRequired: true,
            format: 'date-time',
        },
        FormulierWaardes: {
            type: 'array',
            contains: {
                type: 'FormulierWaarde',
            },
            isRequired: true,
        },
        Dict: {
            type: 'any-of',
            contains: [{
                type: 'dictionary',
                contains: {
                    properties: {
                    },
                },
            }, {
                type: 'null',
            }],
        },
    },
} as const;
