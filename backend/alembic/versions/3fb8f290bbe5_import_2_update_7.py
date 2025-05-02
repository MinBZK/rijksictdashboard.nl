"""import 2 update 7 - fix for volgorde geschatte levensduur

Revsion ID: 3fb8f290bbe5
Revises: 97d667392c2c
Create Date: 2023-02-22 09:59:00

upgrade
script-migration AddVereistToIndicatorlijst AddLockBooleans
downgrade
script-migration AddLockBooleans AddVereistToIndicatorlijst

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "3fb8f290bbe5"
down_revision = "97d667392c2c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    upgrade_query = """

        START TRANSACTION;

        ALTER TABLE "IndicatorLijst" ADD "IsLockable" boolean NOT NULL DEFAULT FALSE;

        ALTER TABLE "Indicator" ADD "IsLockable" boolean NOT NULL DEFAULT FALSE;

        ALTER TABLE "Formulier" ADD "IsLocked" boolean NOT NULL DEFAULT FALSE;

        ALTER TABLE "Antwoord" ADD "IsLocked" boolean NOT NULL DEFAULT FALSE;

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = '5a7fd275-1d3e-455a-9d7b-96ec9214976a', "SecurityStamp" = '73544e53-346f-47a5-aadc-69397efb58f8'
        WHERE "Id" = '258f96f3-ef86-4c00-b9f8-1cee593fd158';

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = '939cd7a9-63b4-447f-a5b1-237aff1315d1', "SecurityStamp" = '3df645c0-ce8f-441f-aec1-7fd1100788ea'
        WHERE "Id" = '971c5b84-ce6f-4d8e-b009-c0fbc9ea452b';

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = '50321f2a-6234-413c-8b8d-60cf85b76ffb', "SecurityStamp" = '696776a7-40d0-4c42-b558-d8e6ac4ab0bc'
        WHERE "Id" = '992dca13-29cf-491c-9b94-4462cd3bb3eb';

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = 'e36b0b56-05f1-4118-8efe-06ab99240b0a', "SecurityStamp" = '2a192426-8540-45eb-bceb-d7fb994eaeed'
        WHERE "Id" = 'bc6eee82-2c77-4c19-9505-1f9a9a5cd0fa';

        UPDATE "AspNetUsers" SET "SecurityStamp" = '43efe5c4-7327-4af8-8936-a2ee36804ea4'
        WHERE "Id" = 'f544b9a8-fd3d-480e-8966-413996ccfaa4';

        INSERT INTO "__EFMigrationsHistory" ("MigrationId", "ProductVersion")
        VALUES ('20230228075546_AddLockBooleans', '6.0.13');

        COMMIT;
        
        UPDATE "public"."Indicator"
        SET "AntwoordTypeId"='2'
        WHERE ("public"."Indicator"."Id" = 93)
        ;
        UPDATE "public"."Indicator"
        SET "AntwoordTypeId"='2'
        WHERE ("public"."Indicator"."Id" = 104)
        ;

        UPDATE "public"."Indicator"
        SET "VerwijderDatum"='0001-01-01 00:00:00', "Titel"='Reden herijking', "Index"='2', "AntwoordTypeId"='4'
        WHERE ("public"."Indicator"."Id" = 105)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='3', "IsLockable"='true'
        WHERE ("public"."Indicator"."Id" = 20)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='4'
        WHERE ("public"."Indicator"."Id" = 33)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='5', "IsLockable"='true'
        WHERE ("public"."Indicator"."Id" = 63)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='5', "IsLockable"='true'
        WHERE ("public"."Indicator"."Id" = 69)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='5', "IsLockable"='true'
        WHERE ("public"."Indicator"."Id" = 70)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='5', "IsLockable"='true'
        WHERE ("public"."Indicator"."Id" = 65)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='5', "IsLockable"='true'
        WHERE ("public"."Indicator"."Id" = 66)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='5', "IsLockable"='true'
        WHERE ("public"."Indicator"."Id" = 68)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='5', "IsLockable"='true'
        WHERE ("public"."Indicator"."Id" = 62)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='5', "IsLockable"='true'
        WHERE ("public"."Indicator"."Id" = 67)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='5', "IsLockable"='true'
        WHERE ("public"."Indicator"."Id" = 64)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='7'
        WHERE ("public"."Indicator"."Id" = 61)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='6'
        WHERE ("public"."Indicator"."Id" = 77)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='6'
        WHERE ("public"."Indicator"."Id" = 76)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='6'
        WHERE ("public"."Indicator"."Id" = 75)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='6'
        WHERE ("public"."Indicator"."Id" = 74)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='6'
        WHERE ("public"."Indicator"."Id" = 72)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='6'
        WHERE ("public"."Indicator"."Id" = 73)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='6'
        WHERE ("public"."Indicator"."Id" = 90)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='6'
        WHERE ("public"."Indicator"."Id" = 89)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='6'
        WHERE ("public"."Indicator"."Id" = 88)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='6'
        WHERE ("public"."Indicator"."Id" = 91)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='6'
        WHERE ("public"."Indicator"."Id" = 87)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='6'
        WHERE ("public"."Indicator"."Id" = 86)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='6'
        WHERE ("public"."Indicator"."Id" = 85)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='6'
        WHERE ("public"."Indicator"."Id" = 84)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='6'
        WHERE ("public"."Indicator"."Id" = 83)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='6'
        WHERE ("public"."Indicator"."Id" = 82)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='6'
        WHERE ("public"."Indicator"."Id" = 81)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='6'
        WHERE ("public"."Indicator"."Id" = 80)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='6'
        WHERE ("public"."Indicator"."Id" = 79)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='6'
        WHERE ("public"."Indicator"."Id" = 78)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='6'
        WHERE ("public"."Indicator"."Id" = 71)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='9'
        WHERE ("public"."Indicator"."Id" = 8)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='10'
        WHERE ("public"."Indicator"."Id" = 9)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='11'
        WHERE ("public"."Indicator"."Id" = 10)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='8'
        WHERE ("public"."Indicator"."Id" = 34)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='13'
        WHERE ("public"."Indicator"."Id" = 19)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='12'
        WHERE ("public"."Indicator"."Id" = 11)
        ;
        UPDATE "public"."Indicator"
        SET "Index"='14'
        WHERE ("public"."Indicator"."Id" = 104)
        ;
        UPDATE "public"."Indicator"
        SET "IsLockable"='true'
        WHERE ("public"."Indicator"."Id" = 18)
        ;
        INSERT INTO "public"."AntwoordOptie" ("Waarde", "IndicatorId", "Index") VALUES ('Aanpassing (business)doelen of eisen','105','0')
        ;
        INSERT INTO "public"."AntwoordOptie" ("Waarde", "IndicatorId", "Index") VALUES ('Implementatie in organisatie','105','1')
        ;
        INSERT INTO "public"."AntwoordOptie" ("Waarde", "IndicatorId", "Index") VALUES ('Overnemen aanbeveling extern advies','105','2')
        ;
        INSERT INTO "public"."AntwoordOptie" ("Waarde", "IndicatorId", "Index") VALUES ('Prijsontwikkeling','105','3')
        ;
        INSERT INTO "public"."AntwoordOptie" ("Waarde", "IndicatorId", "Index") VALUES ('Project-endogene scopewijzigingen','105','4')
        ;
        INSERT INTO "public"."AntwoordOptie" ("Waarde", "IndicatorId", "Index") VALUES ('Tegenvallers binnen project','105','5')
        ;
        INSERT INTO "public"."AntwoordOptie" ("Waarde", "IndicatorId", "Index") VALUES ('Wens van de Tweede Kamer/Eerste Kamer','105','6')
        ;
        INSERT INTO "public"."AntwoordOptie" ("Waarde", "IndicatorId", "Index") VALUES ('Wetswijziging','105','2')
        ;
        UPDATE "public"."Antwoord"
        SET "Waarde" = REPLACE("Waarde",',',';')
        WHERE "IndicatorId" = 105
            AND "Waarde" LIKE '%,%'
        ;
        
    """
    op.execute(upgrade_query)
    op.execute("SET search_path TO public")


def downgrade() -> None:
    downgrade_query = """

        START TRANSACTION;

        ALTER TABLE "IndicatorLijst" DROP COLUMN "IsLockable";

        ALTER TABLE "Indicator" DROP COLUMN "IsLockable";

        ALTER TABLE "Formulier" DROP COLUMN "IsLocked";

        ALTER TABLE "Antwoord" DROP COLUMN "IsLocked";

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = 'd4222ba2-20ba-4752-9e4d-b2a2810f803f', "SecurityStamp" = 'ff88b44d-3778-402e-81b6-f71669887c3d'
        WHERE "Id" = '258f96f3-ef86-4c00-b9f8-1cee593fd158';

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = '437a1f5e-233f-407d-bcc8-665bc36f465e', "SecurityStamp" = '5d4f492a-bbb6-415a-a71e-91198a89cc07'
        WHERE "Id" = '971c5b84-ce6f-4d8e-b009-c0fbc9ea452b';

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = '65bd9279-c25b-43ce-8a46-9cc81cdd0814', "SecurityStamp" = '4b2baeda-3b7a-4d2a-9325-ff13d976c03b'
        WHERE "Id" = '992dca13-29cf-491c-9b94-4462cd3bb3eb';

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = '06357364-0c81-453d-a71d-2f45d39d19da', "SecurityStamp" = '6be0fa40-6ff5-4e0b-b027-735887165b3b'
        WHERE "Id" = 'bc6eee82-2c77-4c19-9505-1f9a9a5cd0fa';

        UPDATE "AspNetUsers" SET "SecurityStamp" = '76fd2940-7795-42f3-b434-17be3f3b104b'
        WHERE "Id" = 'f544b9a8-fd3d-480e-8966-413996ccfaa4';

        DELETE FROM "__EFMigrationsHistory"
        WHERE "MigrationId" = '20230228075546_AddLockBooleans';

        COMMIT;
        
    """
    op.execute(downgrade_query)
    op.execute("SET search_path TO public")
