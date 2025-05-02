import json
from json.decoder import JSONDecodeError

from fastapi import HTTPException, status

from app.types import ProjectAttributeSorting, ProjectFilter
from app.types.jbr_activiteiten_overzicht import ActiviteitMetrics


def __parse(stringified_dict: str | None, parsed_attribute: str) -> list[dict]:
    http_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"{parsed_attribute} value {stringified_dict} is not a valid stringified list",
    )

    try:
        parsed_dict_list = (
            json.loads(stringified_dict) if stringified_dict is not None else []
        )

        # Validate if the result is a list of dictionaries
        assert isinstance(parsed_dict_list, list)

        return parsed_dict_list

    except JSONDecodeError:
        raise http_exception

    except AssertionError:
        raise http_exception


def parse_attributes(
    aggregation_attributes: str | None = None,
) -> list[ActiviteitMetrics]:
    return [
        ActiviteitMetrics(s)
        for s in __parse(aggregation_attributes, "aggregation_attribute")
    ]


def parse_stringified_filters(filters: str | None = None) -> list[ProjectFilter]:
    try:
        return [ProjectFilter(**f) for f in __parse(filters, "filters")]
    except TypeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Value for parameter 'filter' has incorrect format",
        )


def parse_stringified_sorting(
    sorting: str | None = None,
) -> list[ProjectAttributeSorting]:
    try:
        return [ProjectAttributeSorting(**s) for s in __parse(sorting, "sorting")]
    except TypeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Value for parameter 'sorting' has incorrect format",
        )
