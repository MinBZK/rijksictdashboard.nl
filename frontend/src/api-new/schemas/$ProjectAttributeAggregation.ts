/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $ProjectAttributeAggregation = {
    properties: {
        aggregation_attribute: {
            type: 'string',
            isRequired: true,
        },
        values: {
            type: 'array',
            contains: {
                type: 'AttributeAggregation',
            },
            isRequired: true,
        },
    },
} as const;
