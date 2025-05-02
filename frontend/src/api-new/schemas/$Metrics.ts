/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $Metrics = {
    properties: {
        kengetallen: {
            type: 'dictionary',
            contains: {
                properties: {
                },
            },
            isRequired: true,
        },
        ministeries: {
            type: 'array',
            contains: {
                type: 'string',
            },
            isRequired: true,
        },
        projecten: {
            type: 'dictionary',
            contains: {
                type: 'array',
                contains: {
                    type: 'Project',
                },
            },
            isRequired: true,
        },
    },
} as const;
