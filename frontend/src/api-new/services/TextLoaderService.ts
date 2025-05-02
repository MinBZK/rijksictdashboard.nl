/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { StaticContentJson } from '../models/StaticContentJson';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class TextLoaderService {
    /**
     * Get All Content
     * @returns StaticContentJson Successful Response
     * @throws ApiError
     */
    public static getAllContentApiContentGet(): CancelablePromise<StaticContentJson> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/supporting-text',
        });
    }
}

