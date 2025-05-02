import datetime
from dataclasses import dataclass, field
from logging import getLogger
from typing import Any, TypedDict

from sqlalchemy.orm import Session

import app.models as models
import app.schemas as schemas
from app.config.indicatorlijst import attributes_with_multiple_values
from app.controllers.project_collection import ProjectCollection
from app.models.project.core import ProjectViewMetWaardes
from app.services import scraper
from app.types import (
    ActiviteitMetrics,
    ComparisonType,
    ProjectAttributeSorting,
    ProjectFilter,
)

logger = getLogger("uvicorn")


class ProjectResultSet(TypedDict):
    results: list[schemas.ProjectMetAlleMetricsEnIndicatorLijsten]
    total_count: int
    aggregations: list[schemas.ProjectAttributeAggregation]
    ministeries: list[str]
    # metrics: dict
    metrics: ProjectCollection


@dataclass
class Project:
    session: Session
    filters: list[ProjectFilter]
    search: str | None = field(default=None)
    with_attributes: bool = field(default=False)

    def __post_init__(self):
        self.model = (
            models.project.ProjectViewMetWaardes
            if self.with_attributes
            else models.project.ProjectView
        )
        self.project_collection = ProjectCollection(
            filters=self.filters,
            year=None,
            search_activiteit_naam=self.search,
            include_nog_niet_gestart=True,
        )
        self.projecten = self.__get_filtered_projecten_attributes()

    def __get_filtered_projecten_attributes(
        self,
    ) -> list[schemas.ProjectMetAlleMetricsEnIndicatorLijsten]:
        return [p.merged_attributes for p in self.project_collection.projecten_filtered]

    def get_many(
        self,
        limit: int | None,
        return_projects: bool,
        sorting: list[ProjectAttributeSorting],
        aggregation_attributes: list[ActiviteitMetrics] = [],
        page: int = 1,
    ) -> ProjectResultSet:
        sorting = sorting + [ProjectAttributeSorting(attribute="Naam", direction="asc")]

        ministeries = sorted(list(set([p.MinisterieNaam for p in self.projecten])))

        # sort projecten
        def get_sort_key(v):
            sort_value = v.lower() if isinstance(v, str) else v
            return sort_value if sort_value is not None else -999

        sorted_projecten = self.projecten

        for s in reversed(sorting):
            sorted_projecten = sorted(
                sorted_projecten,
                key=lambda x, sorting_attribute=s: get_sort_key(
                    getattr(x, sorting_attribute.attribute)
                ),
                reverse=s.direction != "asc",
            )

        # limit
        if page and limit:
            start = (page - 1) * limit
            end = start + limit
            paginated_projecten = sorted_projecten[start:end]
        else:
            paginated_projecten = sorted_projecten

        return {
            "results": paginated_projecten if return_projects else [],
            "total_count": len(self.projecten),
            "aggregations": self.__get_aggregations(
                aggregation_attributes=aggregation_attributes
            ),
            "ministeries": ministeries,
            "metrics": self.project_collection,
        }

    def get_many_compact(self) -> list[dict]:
        def parse(
            project: ProjectViewMetWaardes,
        ) -> dict:
            body: dict[str, str | dict | list] = {
                "Naam": project.Naam,
                "Ministerie": project.MinisterieNaam,
            }
            for il in project.calculated_attributes.indicatorlijst_waardes:
                il_naam: str = il.IndicatorLijstMeervoudsNaam.value
                il_body = []
                for f in il.Formulier:
                    f_dict = {}
                    for fw in f.FormulierWaardes:
                        f_dict[fw.IndicatorTitel] = fw.Waarde
                    il_body.append(f_dict)
                body[il_naam] = il_body

            return body

        return [parse(p) for p in self.project_collection.projecten_filtered]

    def count_values(
        self,
        attribute: str,
        projecten: list[schemas.ProjectMetAlleMetricsEnIndicatorLijsten] | None = None,
    ) -> dict[str, int]:
        count = {}
        _projecten = projecten if projecten is not None else self.projecten
        projecten_with_attr = [p for p in _projecten if hasattr(p, attribute)]

        for p in projecten_with_attr:
            attribute_value: Any | None = getattr(p, attribute)
            if attribute in attributes_with_multiple_values:
                splitted_values = (
                    attribute_value.split(";") if attribute_value is not None else []
                )
                for v in splitted_values:
                    count[v] = count.get(v, 0) + 1
            elif attribute_value is not None:
                count[attribute_value] = count.get(attribute_value, 0) + 1

        return count

    def __get_aggregations(
        self,
        aggregation_attributes: list[ActiviteitMetrics],
    ) -> list[schemas.ProjectAttributeAggregation]:
        def get_aggregated_values(
            attribute: ActiviteitMetrics,
        ) -> list[schemas.AttributeAggregation]:
            filters = [f for f in self.filters if f.attribute != attribute.value]

            projecten_filtered = [
                p.merged_attributes
                for p in self.project_collection.get_projecten_filtered(filters=filters)
            ]

            value_counts = self.count_values(
                attribute=attribute.value, projecten=projecten_filtered
            )

            return [
                schemas.AttributeAggregation(
                    **{
                        "aggregation_column": attribute,
                        "aggregation_value": aggregation_value,
                        "count": count,
                    }
                )
                for aggregation_value, count in value_counts.items()
            ]

        return [
            schemas.ProjectAttributeAggregation(
                **{
                    "values": get_aggregated_values(attribute=c),
                    "aggregation_attribute": c.value,
                }
            )
            for c in aggregation_attributes
        ]

    @property
    def unique_onderwerpen(self) -> list[str]:
        nested_list = [
            p.Onderwerp.split(";")
            for p in self.project_collection.projecten_unfiltered
            if p.Onderwerp is not None
        ]

        flat_unique_list = [
            onderwerp for onderwerp_list in nested_list for onderwerp in onderwerp_list
        ]

        return sorted(list(set(flat_unique_list)))

    async def get_search_results(self, category: str | None) -> dict:
        projects = [
            schemas.SearchResult(title=p.Naam, id=p.ProjectId, keywords=[])
            for p in self.project_collection.projecten_unfiltered
        ]

        def __apply_search_query(
            candidates: list[schemas.SearchResult], query: str | None
        ):
            matches = [
                c
                for c in candidates
                if c.apply_search_query(query, ComparisonType.EXACT)
            ]
            if len(matches) == 0:
                matches = [
                    c
                    for c in candidates
                    if c.apply_search_query(query, ComparisonType.FUZZY)
                ]
            return matches

        results_in_projects = __apply_search_query(projects, query=self.search)
        results_from_scraper = (
            scraper.get_search_results(self.search) if self.search else []
        )

        # Only show relevant results
        filtered_results = [r for r in results_from_scraper if r.score > 70]

        # Show max 5 relevant results from scraper
        n_results_max = 5
        parsed_results_from_scraper = [
            schemas.SearchResult(title=r.title, id=r.url, url=r.url)
            for r in filtered_results
        ][:n_results_max]

        categories: dict[str, list[schemas.SearchResult]] = {
            "i_strategie": [],
            "projects": results_in_projects,
            "onderwerpen": [],
            "ministeries": [],
            "overig": [],
        }

        for result in parsed_results_from_scraper:
            categories["overig"].append(result)

        if category:
            categories = {
                key: (categories[key] if key == category else []) for key in categories
            }

        for key in categories:
            categories[key] = sorted(
                categories[key],
                key=lambda x: (
                    x.content_element is not None or x.content_element == "",
                    x.content_element,
                ),
            )

        return categories


def validate_project_token(
    request_token: str,
    project_versie_token: str,
    project_versie_token_aanmaakdatum: datetime.datetime,
) -> bool:
    tokens_equal = request_token == project_versie_token
    current_time = datetime.datetime.now(datetime.timezone.utc)
    elapsed_seconds = (
        current_time
        - project_versie_token_aanmaakdatum.replace(tzinfo=datetime.timezone.utc)
    ).total_seconds()
    token_not_expired = elapsed_seconds < 10
    return tokens_equal and token_not_expired
