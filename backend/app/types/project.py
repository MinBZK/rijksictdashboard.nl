from typing import Literal

from pydantic.dataclasses import dataclass


@dataclass
class ProjectFilter:
    attribute: str
    values: list[str]


@dataclass
class ProjectAttributeSorting:
    attribute: str
    direction: Literal["asc", "desc"]
