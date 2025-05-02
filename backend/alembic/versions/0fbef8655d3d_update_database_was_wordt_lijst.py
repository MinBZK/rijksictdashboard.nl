"""update_database_was_wordt_lijst

Revision ID: 0fbef8655d3d
Revises: b6197251e6d2
Create Date: 2023-01-05 16:21:02.575183

"""

import os

from alembic import op

# import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0fbef8655d3d"
down_revision = "b6197251e6d2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    dump_filepath = os.path.abspath(
        "alembic/scripts/20230105153300_upgrade_insert_wwlijst_data.sql"
    )
    with open(dump_filepath, encoding="utf-8") as f:
        sql_file = f.read()
        op.execute(sql_file + "SET search_path TO public")


def downgrade() -> None:
    pass
