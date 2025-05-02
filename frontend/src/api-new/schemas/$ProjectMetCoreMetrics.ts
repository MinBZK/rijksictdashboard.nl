/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $ProjectMetCoreMetrics = {
    properties: {
        ProjectId: {
            type: 'string',
            isRequired: true,
        },
        Naam: {
            type: 'string',
            isRequired: true,
        },
        Slug: {
            type: 'string',
            isRequired: true,
        },
        ProjectVersieId: {
            type: 'number',
            isRequired: true,
        },
        ProjectVersie: {
            type: 'number',
            isRequired: true,
        },
        LegacyProjectId: {
            type: 'any-of',
            contains: [{
                type: 'number',
            }, {
                type: 'null',
            }],
            isRequired: true,
        },
        MinisterieNaam: {
            type: 'string',
            isRequired: true,
        },
        MinisterieAfkorting: {
            type: 'string',
            isRequired: true,
        },
        ProjectVersieWijzigingsDatum: {
            type: 'string',
            isRequired: true,
            format: 'date-time',
        },
        ProjectVersieStatusNaam: {
            type: 'string',
            isRequired: true,
        },
        Onderwerp: {
            type: 'any-of',
            contains: [{
                type: 'string',
            }, {
                type: 'null',
            }],
            isRequired: true,
        },
        ProjectVersieStatusId: {
            type: 'number',
            isRequired: true,
        },
        ProjectStatus: {
            type: 'any-of',
            contains: [{
                type: 'string',
            }, {
                type: 'null',
            }],
            isRequired: true,
        },
        StartDatum: {
            type: 'any-of',
            contains: [{
                type: 'string',
                format: 'date',
            }, {
                type: 'null',
            }],
            isRequired: true,
        },
        PeilDatum: {
            type: 'any-of',
            contains: [{
                type: 'string',
                format: 'date',
            }, {
                type: 'null',
            }],
            isRequired: true,
        },
        OrganisatieNaam: {
            type: 'any-of',
            contains: [{
                type: 'string',
            }, {
                type: 'null',
            }],
            isRequired: true,
        },
        ActiviteitId: {
            type: 'string',
            isRequired: true,
        },
        Ministerie: {
            type: 'string',
            isRequired: true,
        },
        DoorlooptijdActueel: {
            type: 'any-of',
            contains: [{
                type: 'number',
            }, {
                type: 'null',
            }],
            isRequired: true,
        },
        SchattingTotaleKostenHuidigJaar: {
            type: 'number',
            isRequired: true,
        },
        SchattingEinddatumActueel: {
            type: 'any-of',
            contains: [{
                type: 'string',
                format: 'date',
            }, {
                type: 'null',
            }],
            isRequired: true,
        },
        HeeftAcICTAdvies: {
            type: 'string',
            isRequired: true,
        },
        SoortICTActiviteit: {
            type: 'any-of',
            contains: [{
                type: 'string',
            }, {
                type: 'null',
            }],
            isRequired: true,
        },
        MaatschappelijkeBaat: {
            type: 'any-of',
            contains: [{
                type: 'string',
            }, {
                type: 'null',
            }],
            isRequired: true,
        },
    },
} as const;
