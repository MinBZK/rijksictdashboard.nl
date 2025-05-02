/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { HealthStatus } from '../models/HealthStatus';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class HealthCheckService {
    /**
     * Healthcheck
     * @returns HealthStatus Successful Response
     * @throws ApiError
     */
    public static healthcheckHealthGet(): CancelablePromise<Array<HealthStatus>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/health/',
        });
    }
}
