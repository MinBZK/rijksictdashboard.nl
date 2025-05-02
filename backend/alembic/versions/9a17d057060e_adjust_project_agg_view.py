"""adjust project agg view

Revision ID: 9a17d057060e
Revises: 0fbef8655d3d
Create Date: 2023-01-05 16:26:46.778244

"""

import os

from alembic import op

# revision identifiers, used by Alembic.
revision = "9a17d057060e"
down_revision = "0fbef8655d3d"
branch_labels = None
depends_on = None

view_name = "vProjectAgg"


def upgrade() -> None:
    dump_filepath = os.path.abspath("alembic/scripts/v_project_agg2.sql")
    with open(dump_filepath, encoding="utf-8") as f:
        query = f.read()
        op.execute(
            f"""
            drop view if exists "{view_name}"
        """
        )
        op.execute(f"""create view "{view_name}" as ({query})""")


def downgrade() -> None:
    pass
