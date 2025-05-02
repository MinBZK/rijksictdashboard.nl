"""Import v2.0

Revsion ID: f5ef73c7a407
Revises: ad4824c9c1a0
Create Date: 2023-02-14 11:39:00

"""

import os

from alembic import op

# import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "f5ef73c7a407"
down_revision = "ad4824c9c1a0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    import_filepath = os.path.abspath("alembic/scripts/import_v2.0.sql")
    with open(import_filepath, encoding="utf-8") as f:
        sql_file = f.read()
        op.execute(sql_file)
        op.execute("SET search_path TO public")


def downgrade() -> None:
    pass
