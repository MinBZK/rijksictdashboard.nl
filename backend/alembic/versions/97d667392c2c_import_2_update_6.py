"""import 2 update 6 - fix for volgorde geschatte levensduur

Revsion ID: 97d667392c2c
Revises: 43d08b21d647
Create Date: 2023-02-21 12:12:00

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "97d667392c2c"
down_revision = "43d08b21d647"
branch_labels = None
depends_on = None


def upgrade() -> None:
    upgrade_query = """

        UPDATE "public"."AntwoordOptie"
        SET "Waarde"=' 0-5 jaar'
        WHERE ("public"."AntwoordOptie"."Id" = 592)
        ;
        UPDATE "public"."AntwoordOptie"
        SET "Waarde"=' 5-10 jaar'
        WHERE ("public"."AntwoordOptie"."Id" = 593)
        ;
        UPDATE "public"."Indicator"
        SET "AntwoordTypeId"='7'
        WHERE ("public"."Indicator"."Id" = 5)
        ;

    """
    op.execute(upgrade_query)


def downgrade() -> None:
    pass
