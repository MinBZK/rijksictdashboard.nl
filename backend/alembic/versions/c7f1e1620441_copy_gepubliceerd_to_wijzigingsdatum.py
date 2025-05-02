"""Copy gepubliceerd to wijzigingsdatum

Revsion ID: c7f1e1620441
Revises: 54f8f9990fe9
Create Date: 2023-03-17 17:50:00

upgrade
script-migration AddLockBooleans UpdateOrganisaties
downgrade
script-migration UpdateOrganisaties AddLockBooleans

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "c7f1e1620441"
down_revision = "54f8f9990fe9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    upgrade_query = """

        UPDATE public."ProjectVersie" SET "WijzigingsDatum" = converteddata
        FROM 
            (
                SELECT pv_1."Id" AS "ProjectVersieId",
                    TO_DATE(a."Waarde",'YYYY-MM-DD') as converteddata
                FROM ((((("ProjectVersie" pv_1
                     JOIN "FormulierProjectVersie" fpv ON ((fpv."ProjectVersiesId" = pv_1."Id")))
                     JOIN "Project" project ON ((pv_1."ProjectId" = project."Id")))
                     JOIN "Formulier" f ON ((f."Id" = fpv."FormulierenId")))
                     JOIN "Antwoord" a ON ((a."FormulierId" = f."Id")))
                     JOIN "Indicator" i ON ((i."Id" = a."IndicatorId")))
                WHERE "IndicatorId" = 93
            ) as binnen
        WHERE "ProjectVersie"."Id" = "ProjectVersieId"
        
    """
    op.execute(upgrade_query)
    op.execute("SET search_path TO public")


def downgrade() -> None:
    pass
