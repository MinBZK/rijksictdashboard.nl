"""verander indicatortitel beleidsterrein

Revision ID: 92488a2b604a
Revises: b6197251e6d2
Create Date: 2023-01-03 13:18:27.183348

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "92488a2b604a"
down_revision = "b6197251e6d2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    query = """
    update "Indicator"
    set "Titel" = 'Onderwerp'
    where "Titel" = 'Beleidsterrein'
    """
    op.execute(query)


def downgrade() -> None:
    query = """
    update "Indicator"
    set "Titel" = 'Beleidsterrein'
    where "Titel" = 'Onderwerp'
    """
    op.execute(query)
