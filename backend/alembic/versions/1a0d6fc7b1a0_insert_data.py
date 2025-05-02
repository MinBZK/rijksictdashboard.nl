"""insert data

Revision ID: 1a0d6fc7b1a0
Revises: 9982eba1a0e6
Create Date: 2022-11-04 09:25:31.213406

"""

import os

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "1a0d6fc7b1a0"
down_revision = "9982eba1a0e6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "project", sa.Column("omschrijving", sa.types.ARRAY(sa.String), nullable=True)
    )

    dump_filepath = os.path.abspath("alembic/scripts/init_data.sql")
    with open(dump_filepath, encoding="utf-8") as f:
        sql_file = f.read()
        op.execute(sql_file + "SET search_path TO public")
    pass


def downgrade() -> None:
    op.execute("delete from project")
    op.execute("delete from ministerie")
    op.execute("delete from status")
    pass
