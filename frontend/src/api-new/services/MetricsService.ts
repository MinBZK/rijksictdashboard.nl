/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class MetricsService {
    /**
     * Get Activiteiten
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getActiviteitenMetricsActiviteitYearGet({
        year,
    }: {
        year: (number | null),
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/metrics/activiteit/{year}',
            path: {
                'year': year,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
