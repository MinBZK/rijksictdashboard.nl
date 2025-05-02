"""versies publiceren

Revision ID: 061fbf95024d
Revises: 28a6ba75ae93
Create Date: 2022-12-14 11:01:06.408412

"""

import os

from alembic import op

# revision identifiers, used by Alembic.
revision = "061fbf95024d"
down_revision = "28a6ba75ae93"
branch_labels = None
depends_on = None


def upgrade() -> None:
    dump_filepath = os.path.abspath(
        "alembic/scripts/upgrade_addfunctioneelbeheerderrol_setlatestversiontopublished.sql"
    )
    with open(dump_filepath, encoding="utf-8") as f:
        sql_file = f.read()
        op.execute(sql_file)


def downgrade() -> None:
    dump_filepath = os.path.abspath(
        "alembic/scripts/downgrade_setlatestversiontopublished_addfunctioneelbeheerderrol.sql"
    )
    with open(dump_filepath, encoding="utf-8") as f:
        sql_file = f.read()
        op.execute(sql_file)
