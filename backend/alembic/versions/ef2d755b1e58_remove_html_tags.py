"""remove html tags

Revision ID: ef2d755b1e58
Revises: e9ee3b3842ab
Create Date: 2023-04-12 11:36:09.655720

"""

import os

from alembic import op

# revision identifiers, used by Alembic.
revision = "ef2d755b1e58"
down_revision = "e9ee3b3842ab"
branch_labels = None
depends_on = None


def upgrade() -> None:
    dump_filepath = os.path.abspath("alembic/scripts/query_remove_html_tags.sql")
    with open(dump_filepath, encoding="utf-8") as f:
        sql_file = f.read()
        op.execute(sql_file + "; SET search_path TO public")


def downgrade() -> None:
    dump_filepath = os.path.abspath("alembic/scripts/query_undo_html_tag_removal.sql")
    with open(dump_filepath, encoding="utf-8") as f:
        sql_file = f.read()
        op.execute(sql_file + "; SET search_path TO public")
