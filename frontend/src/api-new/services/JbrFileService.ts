/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class JbrFileService {
    /**
     * Get Rapportage
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getRapportageJbrFileYearGet({
        year,
    }: {
        year: number,
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/jbr-file/{year}',
            path: {
                'year': year,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Activiteit
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getActiviteitJbrFileYearActiviteitActiviteitIdGet({
        year,
        activiteitId,
    }: {
        year: number,
        activiteitId: string,
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/jbr-file/{year}/activiteit/{activiteit_id}',
            path: {
                'year': year,
                'activiteit_id': activiteitId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Activiteiten Csv
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getActiviteitenCsvJbrFileActiviteitenYearGet({
        year,
    }: {
        year: number,
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/jbr-file/activiteiten/{year}',
            path: {
                'year': year,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
