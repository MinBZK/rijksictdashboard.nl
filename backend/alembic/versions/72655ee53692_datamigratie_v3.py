"""datamigratie v3

Revision ID: 72655ee53692
Revises: 9dfc3a031b59
Create Date: 2023-04-06 17:19:35.861948

"""

import os

from alembic import op

# revision identifiers, used by Alembic.
revision = "72655ee53692"
down_revision = "9dfc3a031b59"
branch_labels = None
depends_on = None


def upgrade() -> None:
    dump_filepath = os.path.abspath("alembic/scripts/import_3.2.sql")
    with open(dump_filepath, encoding="utf-8") as f:
        sql_file = f.read()
        op.execute(sql_file + "; SET search_path TO public")


def downgrade() -> None:
    pass
