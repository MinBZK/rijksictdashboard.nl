/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $ProjectenMetMetrics = {
    properties: {
        metrics: {
            type: 'Metrics',
            isRequired: true,
        },
        results: {
            type: 'array',
            contains: {
                type: 'ProjectMetCoreMetrics',
            },
            isRequired: true,
        },
        total_count: {
            type: 'number',
            isRequired: true,
        },
        aggregations: {
            type: 'array',
            contains: {
                type: 'ProjectAttributeAggregation',
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
    },
} as const;
