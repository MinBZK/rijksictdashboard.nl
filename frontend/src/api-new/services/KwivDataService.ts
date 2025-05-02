/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { KWIVData } from '../models/KWIVData';
import type { KwivJaar } from '../models/KwivJaar';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class KwivDataService {
    /**
     * Kwiv
     * @returns KWIVData Successful Response
     * @throws ApiError
     */
    public static kwivKwivGet({
        jaar,
        ministerie,
        category,
    }: {
        jaar: KwivJaar,
        ministerie?: (string | null),
        category?: (string | null),
    }): CancelablePromise<KWIVData> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/kwiv/',
            query: {
                'jaar': jaar,
                'ministerie': ministerie,
                'category': category,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
