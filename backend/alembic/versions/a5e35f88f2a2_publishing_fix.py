"""publishing fix

Revision ID: a5e35f88f2a2
Revises: 2a6a2e8efb39
Create Date: 2023-01-18 11:24:10.546525

"""

import os

from alembic import op

# revision identifiers, used by Alembic.
revision = "a5e35f88f2a2"
down_revision = "2a6a2e8efb39"
branch_labels = None
depends_on = None


def upgrade() -> None:
    dump_filepath = os.path.abspath("alembic/scripts/publishing-fix.sql")
    with open(dump_filepath, encoding="utf-8") as f:
        sql_file = f.read()
        op.execute(sql_file)


def downgrade() -> None:
    dump_filepath = os.path.abspath("alembic/scripts/v_project_agg4.sql")
    with open(dump_filepath, encoding="utf-8") as f:
        sql_file = f.read()
        op.execute(sql_file)
