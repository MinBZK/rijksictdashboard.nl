from fuzzywuzzy import fuzz
from pydantic import BaseModel

from app.types import ComparisonType


class SearchResult(BaseModel):
    title: str
    id: str
    keywords: list[str] = []
    content_element: str | None = None
    matched_elements: list[str] | None = None
    matching_score: int | None = None
    url: str | None = None

    def apply_search_query(
        self, query: str | None, comparison_type: ComparisonType
    ) -> bool:
        if not query:
            return False

        keywords = [self.title] + self.keywords
        return any([self.compare_strings(query, k, comparison_type) for k in keywords])

    @staticmethod
    def compare_strings(
        query: str, keyword: str, comparison_type: ComparisonType
    ) -> bool:
        SIMILARITY_THRESHOLD: int = 75

        query = query.lower()
        keyword = keyword.lower()

        if comparison_type == ComparisonType.EXACT:
            return query in keyword
        elif comparison_type == ComparisonType.FUZZY:
            return fuzz.partial_ratio(query, keyword) > SIMILARITY_THRESHOLD


class SearchResults(BaseModel):
    projects: list[SearchResult]
    ministeries: list[SearchResult]
    onderwerpen: list[SearchResult]
    i_strategie: list[SearchResult]
    overig: list[SearchResult]
