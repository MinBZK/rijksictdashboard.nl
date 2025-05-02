/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class IctKostenService {
    /**
     * Kostenstelsels
     * @returns any Successful Response
     * @throws ApiError
     */
    public static kostenstelselsIctKostenGet({
        ministerie,
    }: {
        ministerie?: (string | null),
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/ict-kosten/',
            query: {
                'ministerie': ministerie,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
