"""voeg organisaties toe

Revision ID: 8bfda745eb0c
Revises: 01aad1e940f8
Create Date: 2023-05-09 16:02:16.552827

"""

import sqlalchemy as sa

from app.database.database import Base, SessionLocal


class Ministerie(Base):
    __tablename__ = "Ministerie"

    Id = sa.Column(sa.Integer, primary_key=True)
    Naam = sa.Column(sa.String)
    Afkorting = sa.Column(sa.String)


class Organisatie(Base):
    __tablename__ = "Organisatie"

    Id = sa.Column(sa.Integer, primary_key=True)
    Naam = sa.Column(sa.String)
    MinisterieId = sa.Column(sa.Integer, sa.ForeignKey("Ministerie.Id"))


# revision identifiers, used by Alembic.
revision = "8bfda745eb0c"
down_revision = "01aad1e940f8"
branch_labels = None
depends_on = None


session = SessionLocal()

jenv_organisaties = [
    "Centraal Orgaan opvang Asielzoekers (COA)",
    "Directoraat-Generaal Migratie (DGM)",
    "Directoraat-Generaal Politie en Veiligheidsregio’s (DGPenV)",
    "Directoraat-Generaal Rechtspleging en Rechtshandhaving (DGRR)",
    "Politie",
    "Justitiële ICT Organisatie",
    "Justitiële Informatie Dienst (Justid)",
    "Nationaal Cyber Security Centrum (NCSC)",
    "Raad voor Rechtsbijstand",
    "Raad voor de Kinderbescherming",
]


def upgrade() -> None:
    for naam in jenv_organisaties:
        session.add(Organisatie(**{"Naam": naam, "MinisterieId": 8}))
    session.commit()


def downgrade() -> None:
    pass
