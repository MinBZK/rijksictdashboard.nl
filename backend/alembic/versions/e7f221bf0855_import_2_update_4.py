"""import 2 update 4 - fix for tables not showing

Revsion ID: e7f221bf0855
Revises: f2a09356d07e
Create Date: 2023-02-17 18:30:00

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "e7f221bf0855"
down_revision = "f2a09356d07e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    upgrade_query = """

        INSERT INTO "public"."Antwoord" ("IndicatorId", "Waarde", "FormulierId", "AanmaakDatum", "WijzigingsDatum")
        SELECT
            71,
            '',
            "FormulierId",
            "AanmaakDatum",
            "WijzigingsDatum"
        FROM "public"."Antwoord"
        WHERE "IndicatorId" = 72
        ;

    """
    op.execute(upgrade_query)


def downgrade() -> None:
    pass
