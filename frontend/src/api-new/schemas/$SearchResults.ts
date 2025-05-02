/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $SearchResults = {
    properties: {
        projects: {
            type: 'array',
            contains: {
                type: 'SearchResult',
            },
            isRequired: true,
        },
        ministeries: {
            type: 'array',
            contains: {
                type: 'SearchResult',
            },
            isRequired: true,
        },
        onderwerpen: {
            type: 'array',
            contains: {
                type: 'SearchResult',
            },
            isRequired: true,
        },
        i_strategie: {
            type: 'array',
            contains: {
                type: 'SearchResult',
            },
            isRequired: true,
        },
        overig: {
            type: 'array',
            contains: {
                type: 'SearchResult',
            },
            isRequired: true,
        },
    },
} as const;
