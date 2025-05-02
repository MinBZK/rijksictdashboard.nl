from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.misc import Base


class Ministerie(Base):
    __tablename__ = "Ministerie"

    Id: Mapped[int] = mapped_column(Integer)
    Naam: Mapped[str] = mapped_column(String, primary_key=True)
    Afkorting: Mapped[str] = mapped_column(String)
