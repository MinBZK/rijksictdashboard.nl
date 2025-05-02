"""insert status changes

Revision ID: b6197251e6d2
Revises: f326bb8dd06c
Create Date: 2022-12-14 15:26:12.573095

"""

import os

from alembic import op

# revision identifiers, used by Alembic.
revision = "b6197251e6d2"
down_revision = "f326bb8dd06c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    dump_filepath = os.path.abspath(
        "alembic/scripts/20221214212557_upgrade_addafkortingministerie_insertstatuschanges.sql"
    )
    with open(dump_filepath, encoding="utf-8") as f:
        sql_file = f.read()
        op.execute(sql_file)


def downgrade() -> None:
    dump_filepath = os.path.abspath(
        "alembic/scripts/20221214212557_downgrade_insertstatuschanges_addafkortingministerie.sql"
    )
    with open(dump_filepath, encoding="utf-8") as f:
        sql_file = f.read()
        op.execute(sql_file)
