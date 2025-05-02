import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers.opendata import ExportFormat

client = TestClient(app)


SAMPLE_PROJECT_ID = "0f3bfb17-4c34-48fa-be90-abf94eba9e04"
ENDPOINT_GET_MANY_LIMIT = "project/?limit=20&page=2&search=&filters=%5B%5D&sorting=%5B%7B%22attribute%22%3A%22MinisterieNaam%22%2C%22direction%22%3A%22asc%22%7D%5D&aggregation_attributes=%5B%22MinisterieNaam%22%2C%22Onderwerp%22%2C%22ProjectStatus%22%2C%22HeeftAcICTAdvies%22%2C%22Dienstverlening%22%2C%22MaatschappelijkeBaat%22%5D"  # noqa
ENDPOINT_GET_MANY_NO_LIMIT = "project/?search=&filters=%5B%7B%22attribute%22%3A%22HeeftAcICTAdvies%22%2C%22values%22%3A%5B%22Nee%22%5D%7D%2C%7B%22attribute%22%3A%22MaatschappelijkeBaat%22%2C%22values%22%3A%5B%22Effici%C3%ABntie%22%2C%22Vakmanschap%22%5D%7D%5D&sorting=%5B%7B%22attribute%22%3A%22MinisterieNaam%22%2C%22direction%22%3A%22asc%22%7D%5D&aggregation_attributes=%5B%22MinisterieNaam%22%2C%22Onderwerp%22%2C%22ProjectStatus%22%2C%22HeeftAcICTAdvies%22%2C%22Dienstverlening%22%2C%22MaatschappelijkeBaat%22%5D"  # noqa
FAKE_PROJECT_ID = "e4556fb2-b574-4ff8-aa2b-1253aff70b45"


class TestEndpoints:
    def __test_get_endpoint(
        self, endpoint, params: dict, expected_status_code: int = 200
    ):
        response = client.get(endpoint, params=params)
        assert response.status_code == expected_status_code
        return response

    def test_project_get_many(self):
        # get many
        limit = 3
        response = self.__test_get_endpoint("/project", params={"limit": 3})
        data = response.json()
        projecten = data["results"]
        assert len(projecten) == limit

    @pytest.mark.parametrize(
        "endpoint,expected_status_code,params",
        [
            (ENDPOINT_GET_MANY_LIMIT, 200, {}),
            (ENDPOINT_GET_MANY_NO_LIMIT, 200, {}),
            (f"/project/{SAMPLE_PROJECT_ID}", 200, {}),
            (f"/project/{SAMPLE_PROJECT_ID}", 400, {"token": "fout"}),
            (
                f"/project/{SAMPLE_PROJECT_ID}",
                401,
                {"token": "fout", "project_versie_id": 0},
            ),
            (f"/project/{FAKE_PROJECT_ID}", 404, {}),
            ("ict-kosten", 200, {}),
            ("api/content", 200, {}),
            ("ministerie", 200, {}),
            ("metrics/activiteit/2021", 200, {}),
            ("search/eco", 200, {}),
            (
                f"opendata/spreadsheet/excel/{SAMPLE_PROJECT_ID}",
                200,
                {"export_format": ExportFormat.NESTED.value},
            ),
            (
                f"opendata/spreadsheet/excel/{SAMPLE_PROJECT_ID}",
                200,
                {"export_format": ExportFormat.FLAT.value},
            ),
            ("opendata/spreadsheet/excel", 200, {}),
            ("opendata/spreadsheet/ods", 200, {}),
            ("opendata/json", 200, {}),
            ("jbr-file/2022", 200, {}),
            (f"jbr-file/2022/activiteit/{SAMPLE_PROJECT_ID}", 200, {}),
            ("jbr-file/activiteiten/2022", 200, {}),
            ("kwiv", 200, {"jaar": 2022}),
            ("kwiv", 200, {"jaar": 2023}),
            ("health", 200, {}),
        ],
    )
    def test_get_endpoints(
        self, endpoint: str, expected_status_code: int, params: dict
    ):
        self.__test_get_endpoint(
            endpoint, expected_status_code=expected_status_code, params=params
        )
