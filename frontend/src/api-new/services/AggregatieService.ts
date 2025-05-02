/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class AggregatieService {
    /**
     * Agg Per Attribute
     * @returns any Successful Response
     * @throws ApiError
     */
    public static aggPerAttributeProjectAggregatieAggAttributeGet({
        attribute,
        filters,
    }: {
        attribute: string,
        filters?: (string | null),
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/project-aggregatie/agg/{attribute}',
            path: {
                'attribute': attribute,
            },
            query: {
                'filters': filters,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
