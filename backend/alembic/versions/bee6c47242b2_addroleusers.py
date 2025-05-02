"""addroleusers

Revision ID: bee6c47242b2
Revises: 803853aa50b6
Create Date: 2023-01-06 15:45:00.000000

"""

import os

from alembic import op

# import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "bee6c47242b2"
down_revision = "803853aa50b6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    dump_filepath = os.path.abspath(
        "alembic/scripts/20230106143515_upgrade_insertstatuschanges_addroleusers.sql"
    )
    with open(dump_filepath, encoding="utf-8") as f:
        sql_file = f.read()
        op.execute(sql_file)


def downgrade() -> None:
    dump_filepath = os.path.abspath(
        "alembic/scripts/20230106143515_downgrade_addroleusers_insertstatuschanges.sql"
    )
    with open(dump_filepath, encoding="utf-8") as f:
        sql_file = f.read()
        op.execute(sql_file)
