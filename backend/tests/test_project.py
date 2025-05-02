import datetime

import pytest

from app.controllers.project import validate_project_token


@pytest.mark.parametrize(
    "request_token,project_versie_token,aanmaakdatum,expected_result",
    [
        (
            "a",
            "b",
            datetime.datetime(2019, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc),
            False,
        ),
        (
            "a",
            "a",
            datetime.datetime(2019, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc),
            False,
        ),
        ("a", "a", None, True),
    ],
)
def test_validate_project_token(
    request_token: str,
    project_versie_token: str,
    aanmaakdatum: datetime.datetime | None,
    expected_result: bool,
):
    aanmaakdatum_adjusted = (
        aanmaakdatum
        if aanmaakdatum is not None
        else datetime.datetime.now(datetime.timezone.utc)
    )

    token_is_valid = validate_project_token(
        request_token=request_token,
        project_versie_token=project_versie_token,
        project_versie_token_aanmaakdatum=aanmaakdatum_adjusted,
    )
    assert token_is_valid == expected_result
