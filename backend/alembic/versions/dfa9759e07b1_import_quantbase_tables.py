"""import quantbase tables

Revision ID: dfa9759e07b1
Revises: 1a0d6fc7b1a0
Create Date: 2022-11-18 11:43:39.969493

"""

import os

from sqlalchemy.sql import quoted_name

from alembic import op

# revision identifiers, used by Alembic.
revision = "dfa9759e07b1"
down_revision = "1a0d6fc7b1a0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    dump_filepath = os.path.abspath("alembic/scripts/create_quantbase_tables.sql")
    with open(dump_filepath, encoding="utf-8") as f:
        sql_file = f.read()
        op.execute(sql_file + "SET search_path TO public")


def downgrade() -> None:
    created_tables = [
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
        "StatusChange",
        "ProjectVersie",
        "AspNetRoles",
        "Indicator",
        "Formulier",
        "AspNetUsers",
        "IndicatorLijst",
        "Project",
    ]
    for table in created_tables:
        op.drop_table(quoted_name(table, quote=True))
