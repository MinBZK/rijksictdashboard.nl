/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Metrics } from './Metrics';
import type { ProjectAttributeAggregation } from './ProjectAttributeAggregation';
import type { ProjectMetCoreMetrics } from './ProjectMetCoreMetrics';
export type ProjectenMetMetrics = {
    metrics: Metrics;
    results: Array<ProjectMetCoreMetrics>;
    total_count: number;
    aggregations: Array<ProjectAttributeAggregation>;
    ministeries: Array<string>;
};

