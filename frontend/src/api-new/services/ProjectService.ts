/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Project } from '../models/Project';
import type { ProjectenMetMetrics } from '../models/ProjectenMetMetrics';
import type { ProjectMetAlleMetricsEnIndicatorLijsten } from '../models/ProjectMetAlleMetricsEnIndicatorLijsten';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ProjectService {
    /**
     * Get Many
     * @returns ProjectenMetMetrics Successful Response
     * @throws ApiError
     */
    public static getManyProjectGet({
        limit,
        page = 1,
        search,
        getProjects = true,
        filters,
        sorting,
        aggregationAttributes,
    }: {
        limit?: (number | null),
        page?: number,
        search?: (string | null),
        getProjects?: boolean,
        filters?: (string | null),
        sorting?: (string | null),
        aggregationAttributes?: (string | null),
    }): CancelablePromise<ProjectenMetMetrics> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/project/',
            query: {
                'limit': limit,
                'page': page,
                'search': search,
                'get_projects': getProjects,
                'filters': filters,
                'sorting': sorting,
                'aggregation_attributes': aggregationAttributes,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get One
     * @returns ProjectMetAlleMetricsEnIndicatorLijsten Successful Response
     * @throws ApiError
     */
    public static getOneProjectUnparsedProjectIdGet({
        unparsedProjectId,
        isLegacyId = false,
        projectVersieId,
        token,
    }: {
        unparsedProjectId: string,
        isLegacyId?: boolean,
        projectVersieId?: (number | null),
        token?: (string | null),
    }): CancelablePromise<ProjectMetAlleMetricsEnIndicatorLijsten> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/project/{unparsed_project_id}',
            path: {
                'unparsed_project_id': unparsedProjectId,
            },
            query: {
                'is_legacy_id': isLegacyId,
                'project_versie_id': projectVersieId,
                'token': token,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Laatst Gewijzigd
     * @returns Project Successful Response
     * @throws ApiError
     */
    public static laatstGewijzigdProjectLaatstGewijzigdAantalGet({
        aantal,
    }: {
        aantal: number,
    }): CancelablePromise<Array<Project>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/project/laatst-gewijzigd/{aantal}',
            path: {
                'aantal': aantal,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
