"""add ministerie table

Revision ID: 6178c8882784
Revises: f340bda4ea4d
Create Date: 2022-11-30 14:59:47.135553

"""

# import sqlalchemy as sa
import os

from alembic import op

# revision identifiers, used by Alembic.
revision = "6178c8882784"
down_revision = "f340bda4ea4d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    dump_filepath = os.path.abspath("alembic/scripts/add_ministerie.sql")
    with open(dump_filepath, encoding="utf-8") as f:
        sql_file = f.read()
        op.execute(sql_file)


def downgrade() -> None:
    op.drop_column(table_name="AspNetUsers", column_name="MinisterieId")
    op.drop_table(table_name="Ministerie")
