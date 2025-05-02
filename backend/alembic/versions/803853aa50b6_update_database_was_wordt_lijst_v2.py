"""update_database_was_wordt_lijst_v2

Revision ID: 803853aa50b6
Revises: 9a17d057060e
Create Date: 2023-01-06 13:52:00.000000

"""

import os

from alembic import op

# import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "803853aa50b6"
down_revision = "9a17d057060e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    dump_filepath = os.path.abspath(
        "alembic/scripts/20230106135200_upgrade_insert_wwlijst_data_v2.sql"
    )
    with open(dump_filepath, encoding="utf-8") as f:
        sql_file = f.read()
        op.execute(sql_file + "SET search_path TO public")


def downgrade() -> None:
    pass
