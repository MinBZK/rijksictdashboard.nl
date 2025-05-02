from enum import Enum


class ComparisonType(str, Enum):
    EXACT = "exact"
    FUZZY = "fuzzy"
