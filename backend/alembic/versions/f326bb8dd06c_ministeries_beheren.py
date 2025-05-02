"""ministeries beheren

Revision ID: f326bb8dd06c
Revises: 061fbf95024d
Create Date: 2022-12-14 15:26:12.573095

"""

import os

from alembic import op

# revision identifiers, used by Alembic.
revision = "f326bb8dd06c"
down_revision = "061fbf95024d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    dump_filepath = os.path.abspath(
        "alembic/scripts/upgrade_setlatestversiontopublished_addafkortingministerie.sql"
    )
    with open(dump_filepath, encoding="utf-8") as f:
        sql_file = f.read()
        op.execute(sql_file)


def downgrade() -> None:
    dump_filepath = os.path.abspath(
        "alembic/scripts/downgrade_addafkortingministerie_setlatestversiontopublished.sql"
    )
    with open(dump_filepath, encoding="utf-8") as f:
        sql_file = f.read()
        op.execute(sql_file)
