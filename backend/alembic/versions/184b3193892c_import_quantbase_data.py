"""import quantbase data

Revision ID: 184b3193892c
Revises: dfa9759e07b1
Create Date: 2022-11-18 11:51:00.043179

"""

import os

from alembic import op

# revision identifiers, used by Alembic.
revision = "184b3193892c"
down_revision = "dfa9759e07b1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    dump_filepath = os.path.abspath("alembic/scripts/import_quantbase_data.sql")
    with open(dump_filepath, encoding="utf-8") as f:
        sql_file = f.read()
        op.execute(sql_file + "SET search_path TO public")


def downgrade() -> None:
    tables = [
        "__EFMigrationsHistory",
        "GebruikerProject",
        "Antwoord",
        "AntwoordOptie",
        "AspNetRoleClaims",
        "AspNetUserClaims",
        "AspNetUserLogins",
        "AspNetUserRoles",
        "AspNetUserTokens",
        "FormulierProjectVersie",
        "ProjectVersie",
        "AspNetRoles",
        "Indicator",
        "Formulier",
        "AspNetUsers",
        "IndicatorLijst",
        "Project",
    ]
    for table in tables:
        op.execute(f"""delete from "{table}" """)
