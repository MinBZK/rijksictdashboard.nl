"""datamigratie update

Revision ID: 9dfc3a031b59
Revises: 97d4891d0b44
Create Date: 2023-04-05 16:47:04.867695

"""

import os

from alembic import op

# revision identifiers, used by Alembic.
revision = "9dfc3a031b59"
down_revision = "97d4891d0b44"
branch_labels = None
depends_on = None


def upgrade() -> None:
    dump_filepath = os.path.abspath("alembic/scripts/import_3.1.sql")
    with open(dump_filepath, encoding="utf-8") as f:
        sql_file = f.read()
        op.execute(sql_file + "; SET search_path TO public")


def downgrade() -> None:
    pass
