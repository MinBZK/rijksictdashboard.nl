"""import 2 update 3

Revsion ID: f2a09356d07e
Revises: 92007a2a8ebe
Create Date: 2023-02-17 17:30:00

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "f2a09356d07e"
down_revision = "92007a2a8ebe"
branch_labels = None
depends_on = None


def upgrade() -> None:
    upgrade_query = """

        UPDATE "public"."Indicator"
        SET "Titel"='Daadwerkelijk overig materieel'
        WHERE ("public"."Indicator"."Id" = 68)
        ;
        UPDATE "public"."Indicator"
        SET "Titel"='Actueel geschat overig materieel'
        WHERE ("public"."Indicator"."Id" = 67)
        ;
        UPDATE "public"."Indicator"
        SET "AntwoordTypeId"='7'
        WHERE ("public"."Indicator"."Id" = 39)
        ;
        UPDATE "public"."Indicator"
        SET "AntwoordTypeId"='7'
        WHERE ("public"."Indicator"."Id" = 61)
        ;
        UPDATE "public"."Indicator"
        SET "AntwoordTypeId"='7'
        WHERE ("public"."Indicator"."Id" = 33)
        ;
        UPDATE "public"."Indicator"
        SET "Titel"='Kosten in miljoenen'
        WHERE ("public"."Indicator"."Id" = 62)
        ;


        UPDATE "public"."Tabeleigenschap"
        SET "Titel"='Overig materieel'
        WHERE ("public"."Tabeleigenschap"."Id" = 25)
        ;

    """
    op.execute(upgrade_query)


def downgrade() -> None:
    pass
