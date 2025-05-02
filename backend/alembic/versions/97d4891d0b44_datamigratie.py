"""datamigratie

Revision ID: 97d4891d0b44
Revises: 9e677453d970
Create Date: 2023-04-04 09:59:37.418079

"""

import os

from alembic import op

# revision identifiers, used by Alembic.
revision = "97d4891d0b44"
down_revision = "9e677453d970"
branch_labels = None
depends_on = None


def upgrade() -> None:
    dump_filepath = os.path.abspath("alembic/scripts/import_3.sql")
    with open(dump_filepath, encoding="utf-8") as f:
        sql_file = f.read()
        op.execute(sql_file + "; SET search_path TO public")


def downgrade() -> None:
    pass
