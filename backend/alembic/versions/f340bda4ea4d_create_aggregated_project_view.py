"""create aggregated project view

Revision ID: f340bda4ea4d
Revises: 184b3193892c
Create Date: 2022-11-18 15:46:10.645099

"""

import os

from alembic import op

# revision identifiers, used by Alembic.
revision = "f340bda4ea4d"
down_revision = "184b3193892c"
branch_labels = None
depends_on = None

view_name = "vProjectAgg"


def upgrade() -> None:
    dump_filepath = os.path.abspath("alembic/scripts/v_project_agg.sql")
    with open(dump_filepath, encoding="utf-8") as f:
        query = f.read()
        create_view_query = f"""create view "{view_name}" as ({query})"""
        op.execute(create_view_query)


def downgrade() -> None:
    drop_view_query = f"""drop view "{view_name}" """
    op.execute(drop_view_query)
