/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Ministerie } from '../models/Ministerie';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class MinisterieService {
    /**
     * Get All
     * @returns Ministerie Successful Response
     * @throws ApiError
     */
    public static getAllMinisterieGet(): CancelablePromise<Array<Ministerie>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/ministerie/',
        });
    }
}
