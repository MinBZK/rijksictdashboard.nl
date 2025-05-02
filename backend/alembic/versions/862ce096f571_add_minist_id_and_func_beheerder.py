"""add_minist_id_and_func_beheerder

Revision ID: 862ce096f571
Revises: 6178c8882784
Create Date: 2022-12-07 11:17:02.765967

"""

import os

from alembic import op

# revision identifiers, used by Alembic.
revision = "862ce096f571"
down_revision = "6178c8882784"
branch_labels = None
depends_on = None


def upgrade() -> None:
    dump_filepath = os.path.abspath(
        "alembic/scripts/up_ministerieid_and_beheerderrol.sql"
    )
    with open(dump_filepath, encoding="utf-8") as f:
        sql_file = f.read()
        op.execute(sql_file)


def downgrade() -> None:
    dump_filepath = os.path.abspath(
        "alembic/scripts/down_ministerieid_and_beheerderrol.sql"
    )
    with open(dump_filepath, encoding="utf-8") as f:
        sql_file = f.read()
        op.execute(sql_file)
