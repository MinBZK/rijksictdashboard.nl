"""adjust project view aggregation

Revision ID: 3c823d381c61
Revises: 2a7ef7f4ce8c
Create Date: 2023-01-06 17:00:31.859213

"""

import os

from alembic import op

# revision identifiers, used by Alembic.
revision = "3c823d381c61"
down_revision = "2a7ef7f4ce8c"
branch_labels = None
depends_on = None


view_name = "vProjectAgg"


def upgrade() -> None:
    dump_filepath = os.path.abspath("alembic/scripts/v_project_agg3.sql")
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
