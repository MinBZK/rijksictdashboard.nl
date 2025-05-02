from sqlalchemy import select

from app.database.database import SessionLocal
from app.models.project import ProjectViewMetWaardes
from app.types import Publicatiestatus
from app.util.logger import get_logger

logger = get_logger(__name__)


class ProjectGetter:
    def __init__(self, project_id: str | None = None, year: int | None = None):
        self.__project_view = ProjectViewMetWaardes
        self.__project_id = project_id
        self.__year = year
        self.projecten = self.__get_projecten()

    def __get_data(self) -> list[ProjectViewMetWaardes]:
        session = SessionLocal()
        stmt = select(self.__project_view).where(
            self.__project_view.ProjectVersieStatusNaam == Publicatiestatus.GEPUBLICEERD
        )
        if self.__project_id:
            stmt = stmt.where(self.__project_view.ProjectId == self.__project_id)

        return list(session.execute(stmt).scalars())

    def get_project_by_id(self, activiteit_id: str) -> ProjectViewMetWaardes | None:
        matched = [p for p in self.projecten if p.ProjectId == activiteit_id]
        if len(matched) == 1:
            return matched[0]

    def __get_projecten(self) -> list[ProjectViewMetWaardes]:
        projecten = self.__get_data()
        for p in projecten:
            p.set_calculated_attributes(year=self.__year)

        return projecten


__all__ = ["ProjectGetter"]
