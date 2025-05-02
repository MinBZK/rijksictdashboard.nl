"""update project view

Revision ID: 2a6a2e8efb39
Revises: 3c823d381c61
Create Date: 2023-01-09 10:08:39.321098

"""

import os

from alembic import op

# revision identifiers, used by Alembic.
revision = "2a6a2e8efb39"
down_revision = "3c823d381c61"
branch_labels = None
depends_on = None


view_name = "vProjectAgg"


def set_view(sql_script_path: str):
    dump_filepath = os.path.abspath(sql_script_path)
    with open(dump_filepath, encoding="utf-8") as f:
        query = f.read()
        op.execute(
            f"""
            drop view if exists "{view_name}"
        """
        )
        op.execute(f"""create view "{view_name}" as ({query})""")


def upgrade() -> None:
    set_view("alembic/scripts/v_project_agg4.sql")


def downgrade() -> None:
    set_view("alembic/scripts/v_project_agg3.sql")
