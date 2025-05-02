/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $KWIVData = {
    properties: {
        datapoints: {
            type: 'array',
            contains: {
                type: 'ChartdataPoint',
            },
            isRequired: true,
        },
        available_ministeries: {
            type: 'array',
            contains: {
                type: 'string',
            },
            isRequired: true,
        },
        available_categories: {
            type: 'array',
            contains: {
                type: 'string',
            },
            isRequired: true,
        },
    },
} as const;
