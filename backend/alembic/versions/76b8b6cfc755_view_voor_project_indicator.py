"""view voor project indicator

Revision ID: 76b8b6cfc755
Revises: 92488a2b604a
Create Date: 2023-01-03 13:51:38.362089

"""

import os

from alembic import op

# revision identifiers, used by Alembic.
revision = "76b8b6cfc755"
down_revision = "92488a2b604a"
branch_labels = None
depends_on = None

view_name = "vProjectIndicator"


def upgrade() -> None:
    dump_filepath = os.path.abspath("alembic/scripts/v_project_indicator.sql")
    with open(dump_filepath, encoding="utf-8") as f:
        query = f.read()
        create_view_query = f"""create view "{view_name}" as ({query})"""
        op.execute(create_view_query)


def downgrade() -> None:
    drop_view_query = f"""drop view if exists "{view_name}" """
    op.execute(drop_view_query)
