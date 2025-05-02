/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ExportFormat } from '../models/ExportFormat';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class OpenDataService {
    /**
     * Project Compact
     * @returns any Successful Response
     * @throws ApiError
     */
    public static projectCompactOpendataJsonGet(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/opendata/json',
        });
    }
    /**
     * Get Activiteit
     * @returns any xlsx
     * @throws ApiError
     */
    public static getActiviteitOpendataSpreadsheetSpreadsheetTypeProjectIdGet({
        projectId,
        spreadsheetType,
        // @ts-ignore
        exportFormat = 'nested',
    }: {
        projectId: string,
        spreadsheetType: 'excel' | 'ods',
        exportFormat?: ExportFormat,
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/opendata/spreadsheet/{spreadsheet_type}/{project_id}',
            path: {
                'project_id': projectId,
                'spreadsheet_type': spreadsheetType,
            },
            query: {
                'export_format': exportFormat,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Alle Activiteiten
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getAlleActiviteitenOpendataSpreadsheetSpreadsheetTypeGet({
        spreadsheetType,
        year,
    }: {
        spreadsheetType: 'excel' | 'ods',
        year?: (number | null),
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/opendata/spreadsheet/{spreadsheet_type}',
            path: {
                'spreadsheet_type': spreadsheetType,
            },
            query: {
                'year': year,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
