/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { SearchResults } from '../models/SearchResults';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ZoekenService {
    /**
     * Search
     * @returns SearchResults Successful Response
     * @throws ApiError
     */
    public static searchSearchSearchQueryGet({
        searchQuery,
        category,
    }: {
        searchQuery: string,
        category?: string,
    }): CancelablePromise<SearchResults> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/search/{search_query}',
            path: {
                'search_query': searchQuery,
            },
            query: {
                'category': category,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
