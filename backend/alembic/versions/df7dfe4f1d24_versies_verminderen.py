"""versies verminderen

Revision ID: df7dfe4f1d24
Revises: a5e35f88f2a2
Create Date: 2023-02-01 23:49:21

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "df7dfe4f1d24"
down_revision = "a5e35f88f2a2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    upgrade_query = """
        START TRANSACTION;

        ALTER TABLE "ProjectVersie" ADD "IsAfgesloten" boolean NOT NULL DEFAULT FALSE;

        ALTER TABLE "Formulier" ADD "WijzigingsDatum" timestamp without time zone NOT NULL DEFAULT TIMESTAMP '0001-01-01 00:00:00';

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = '8fca1f1e-c7df-4b69-a091-89a1b9a34e34', "SecurityStamp" = '47b9c740-99ad-49aa-b5e0-aabdabcac066'
        WHERE "Id" = '258f96f3-ef86-4c00-b9f8-1cee593fd158';

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = '562e95d1-0cce-4364-ae45-619d1c750bd1', "SecurityStamp" = '1f98ccc3-2827-4a6f-99e1-106bf0f66b94'
        WHERE "Id" = '971c5b84-ce6f-4d8e-b009-c0fbc9ea452b';

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = '6b86bf55-0e1b-4d03-a145-0febf2c89d5f', "SecurityStamp" = 'aeca4c1f-172d-4e4a-94cf-3cd0dd502294'
        WHERE "Id" = '992dca13-29cf-491c-9b94-4462cd3bb3eb';

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = '041c1bdb-01c6-4188-b457-52e201fbbe15', "SecurityStamp" = '2b6d4c23-b1b0-4b1a-8588-89e1043a30a6'
        WHERE "Id" = 'bc6eee82-2c77-4c19-9505-1f9a9a5cd0fa';

        UPDATE "AspNetUsers" SET "SecurityStamp" = '1114de1f-7fef-490a-b948-e876d62d2115'
        WHERE "Id" = 'f544b9a8-fd3d-480e-8966-413996ccfaa4';

        UPDATE "public"."ProjectVersie" set "IsAfgesloten" = true;

        UPDATE "public"."Indicator" SET "AntwoordType" = 8, "Toelichting" = 'Bedrag in miljoenen' WHERE "Id" BETWEEN 60 AND 65;

        INSERT INTO "__EFMigrationsHistory" ("MigrationId", "ProductVersion")
        VALUES ('20230201234921_AddIsAfgeslotenToProjectVersie', '6.0.10');
        COMMIT;
    """
    op.execute(upgrade_query)


def downgrade() -> None:
    downgrade_query = """
        START TRANSACTION;

        ALTER TABLE "ProjectVersie" DROP COLUMN "IsAfgesloten";

        ALTER TABLE "Formulier" DROP COLUMN "WijzigingsDatum";

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = 'ed6b82f3-4df6-48af-8dd7-4e554037b1d0', "SecurityStamp" = '2ad5cc16-ce29-40ac-9d45-a45f9c4b4fc3'
        WHERE "Id" = '258f96f3-ef86-4c00-b9f8-1cee593fd158';

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = 'd503eb54-3963-465a-a5bd-ad6120448184', "SecurityStamp" = 'f7e04db4-5908-4146-b95d-af45fd1ec7fb'
        WHERE "Id" = '971c5b84-ce6f-4d8e-b009-c0fbc9ea452b';

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = '410d0b75-a3a6-444e-b89e-2a7978279633', "SecurityStamp" = '1e61b369-2221-4194-948f-6ed3879c20fc'
        WHERE "Id" = '992dca13-29cf-491c-9b94-4462cd3bb3eb';

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = 'fd69d752-778d-44c1-8f52-ae04745b6b46', "SecurityStamp" = '032453b1-04d6-4cb1-8e38-10bb41420ffa'
        WHERE "Id" = 'bc6eee82-2c77-4c19-9505-1f9a9a5cd0fa';

        UPDATE "AspNetUsers" SET "SecurityStamp" = 'd464a27c-b182-4b41-b740-f5e4e5426d37'
        WHERE "Id" = 'f544b9a8-fd3d-480e-8966-413996ccfaa4';

        UPDATE "public"."Indicator" SET "AntwoordType" = 1, "Toelichting" = NULL WHERE "Id" BETWEEN 60 AND 65;

        DELETE FROM "__EFMigrationsHistory"
        WHERE "MigrationId" = '20230201234921_AddIsAfgeslotenToProjectVersie';

        COMMIT;
    """
    op.execute(downgrade_query)
