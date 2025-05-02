"""create project table

Revision ID: 9982eba1a0e6
Revises:
Create Date: 2022-10-31 11:31:35.449887

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "9982eba1a0e6"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "ministerie",
        sa.Column("ministerie_id", sa.Integer, primary_key=True),
        sa.Column("afkorting", sa.String, nullable=False, unique=True),
        sa.Column("toegevoegd_op", sa.DateTime, nullable=False),
        sa.Column("gewijzigd_op", sa.DateTime, nullable=True),
    )

    op.create_table(
        "status",
        sa.Column("status_id", sa.Integer, primary_key=True),
        sa.Column("omschrijving", sa.String, nullable=False, unique=True),
        sa.Column("toegevoegd_op", sa.DateTime, nullable=False),
        sa.Column("gewijzigd_op", sa.DateTime, nullable=True),
    )

    op.create_table(
        "project",
        sa.Column("project_id", sa.Integer, primary_key=True),
        sa.Column("naam", sa.String, nullable=False, unique=True),
        sa.Column("startdatum", sa.DateTime, nullable=False),
        sa.Column("einddatum_initieel", sa.DateTime, nullable=False),
        sa.Column("einddatum_huidig", sa.DateTime, nullable=False),
        sa.Column("kosten_meerjarig_geschat_initieel", sa.Float, nullable=False),
        sa.Column("prognose_toekomstige_kosten", sa.Float, nullable=False),
        sa.Column("uitgaven_cumulatief", sa.Float, nullable=False),
        sa.Column("status_id", sa.Integer, sa.ForeignKey("status.status_id")),
        sa.Column(
            "ministerie_id", sa.Integer, sa.ForeignKey("ministerie.ministerie_id")
        ),
        sa.Column("toegevoegd_op", sa.DateTime, nullable=False),
        sa.Column("gewijzigd_op", sa.DateTime, nullable=True),
    )
    pass


def downgrade() -> None:
    op.drop_table("project")
    op.drop_table("ministerie")
    op.drop_table("status")
    pass
