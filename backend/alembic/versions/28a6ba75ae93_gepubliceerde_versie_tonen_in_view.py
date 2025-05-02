"""gepubliceerde versie tonen in view

Revision ID: 28a6ba75ae93
Revises: 862ce096f571
Create Date: 2022-12-13 12:07:10.928871

"""

import os

from alembic import op

# revision identifiers, used by Alembic.
revision = "28a6ba75ae93"
down_revision = "862ce096f571"
branch_labels = None
depends_on = None


view_name = "vProjectAggStatus"


def upgrade() -> None:
    dump_filepath = os.path.abspath("alembic/scripts/v_project_agg_status.sql")
    with open(dump_filepath, encoding="utf-8") as f:
        query = f.read()
        create_view_query = f"""create view "{view_name}" as ({query})"""
        op.execute(create_view_query)


def downgrade() -> None:
    drop_view_query = f"""drop view "{view_name}" """
    op.execute(drop_view_query)
