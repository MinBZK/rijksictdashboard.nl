"""missende baten toevoegen

Revision ID: 01aad1e940f8
Revises: f56256f4f19f
Create Date: 2023-04-16 20:05:00

upgrade script command:
script-migration AddLockedToVersieAndStartedToProject AddMissendeBaten

downgrade script command:
script-migration AddMissendeBaten AddLockedToVersieAndStartedToProject

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "01aad1e940f8"
down_revision = "f56256f4f19f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    upgrade_query = """
        START TRANSACTION;

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = '7d80569f-55f9-4d36-8b51-a3fecb9de6da', "SecurityStamp" = 'c8a46bad-e3fe-47da-b515-34c44ef0efdc'
        WHERE "Id" = '258f96f3-ef86-4c00-b9f8-1cee593fd158';

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = 'e47452c6-253b-4803-8e68-22fde64f02ba', "SecurityStamp" = '30cca5c9-6f11-448e-ae5b-c45c07bb8ce2'
        WHERE "Id" = '971c5b84-ce6f-4d8e-b009-c0fbc9ea452b';

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = 'ab92abb9-dd3b-4bd9-ac2a-e4599fac7842', "SecurityStamp" = '7e36da01-c1d2-4022-ae2a-d0c009174c82'
        WHERE "Id" = '992dca13-29cf-491c-9b94-4462cd3bb3eb';

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = 'f3fd46ba-ee98-44b0-b625-68b87cf53e02', "SecurityStamp" = '14b9fa99-1c5f-4f14-9e3a-b2e55a9b25d8'
        WHERE "Id" = 'bc6eee82-2c77-4c19-9505-1f9a9a5cd0fa';

        UPDATE "AspNetUsers" SET "SecurityStamp" = 'b9f1a101-5cfb-4490-a6e3-da97727ef3b2'
        WHERE "Id" = 'f544b9a8-fd3d-480e-8966-413996ccfaa4';

        --98	Kwantitatief incidenteel
        --99	Kwantitatief jaar

        --Landelijk Meetnet Water 2 (LMW2)
        --ProjectId:	37f2c0a1-737a-4599-8ed3-41fcdb4b0754
        --VersieId: 	198

        INSERT INTO "public"."Formulier" ("Id", "Nummer", "Status", "AanmaakDatum", "GebruikerId", "IndicatorLijstId", "WijzigingsDatum", "IsLocked")
        VALUES ('90b08962-a412-4a80-b080-23f2f732a5a0', 0, 0, '2023-04-13 00:00:00', NULL, '64a37ba4-f636-423a-aa6f-85e5991baae0', '2023-04-13 00:00:00', false);

        INSERT INTO "public"."FormulierProjectVersie" ("FormulierenId", "ProjectVersiesId") VALUES ('90b08962-a412-4a80-b080-23f2f732a5a0','198');

        INSERT INTO "public"."Antwoord" ("IndicatorId", "Waarde", "FormulierId", "AanmaakDatum", "WijzigingsDatum", "IsLocked") VALUES (99, '0.00', '90b08962-a412-4a80-b080-23f2f732a5a0', '2023-04-13 00:00:00', '2023-04-13 00:00:00', false);
        INSERT INTO "public"."Antwoord" ("IndicatorId", "Waarde", "FormulierId", "AanmaakDatum", "WijzigingsDatum", "IsLocked") VALUES (98, '0.00', '90b08962-a412-4a80-b080-23f2f732a5a0', '2023-04-13 00:00:00', '2023-04-13 00:00:00', false);
        INSERT INTO "public"."Antwoord" ("IndicatorId", "Waarde", "FormulierId", "AanmaakDatum", "WijzigingsDatum", "IsLocked") VALUES (5, 'De informatievoorziening via het LMW is essentieel voor tal van werkprocessen binnen RWS. Dat zijn voor een deel missie kritieke processen: het sluiten van de stormvloedkeringen, de hoog- en laagwaterberichtgeving en het afgeven van getijpoorten voor de grote zeehavens. Daarnaast voor processen zoals het operationeel peilbeheer, het nakomen internationale en regionale afspraken, bepalen van de hydraulische randvoorwaarden voor waterkeringen en de begeleiding van de scheepvaart.\nDe missiekritieke processen stellen hoge eisen aan de beschikbaarheid van actuele en betrouwbare meetgegevens. Door uitvoering van het project LMW2 kan het meetnet aan die eisen ook de komende 15 jaar voldoen. Omdat het een vervanging vanuit continuiteitsoogpunt betreft, is er geen sprake van kwantitatieve baten, maar alleen kwalitatieve baten. De kwalitatieve baten zijn niet in geld uit te drukken.', '90b08962-a412-4a80-b080-23f2f732a5a0', '2023-04-13 00:00:00', '2023-04-13 00:00:00', false);


        INSERT INTO "public"."Formulier" ("Id", "Nummer", "Status", "AanmaakDatum", "GebruikerId", "IndicatorLijstId", "WijzigingsDatum", "IsLocked")
        VALUES ('46a993a3-5172-4850-87e0-005bbda75828', 0, 0, '2023-04-13 00:00:00', NULL, '64a37ba4-f636-423a-aa6f-85e5991baae0', '2023-04-13 00:00:00', false);

        INSERT INTO "public"."FormulierProjectVersie" ("FormulierenId", "ProjectVersiesId") VALUES ('46a993a3-5172-4850-87e0-005bbda75828','198');

        INSERT INTO "public"."Antwoord" ("IndicatorId", "Waarde", "FormulierId", "AanmaakDatum", "WijzigingsDatum", "IsLocked") VALUES (99, '0.00', '46a993a3-5172-4850-87e0-005bbda75828', '2023-04-13 00:00:00', '2023-04-13 00:00:00', false);
        INSERT INTO "public"."Antwoord" ("IndicatorId", "Waarde", "FormulierId", "AanmaakDatum", "WijzigingsDatum", "IsLocked") VALUES (98, '0.00', '46a993a3-5172-4850-87e0-005bbda75828', '2023-04-13 00:00:00', '2023-04-13 00:00:00', false);
        INSERT INTO "public"."Antwoord" ("IndicatorId", "Waarde", "FormulierId", "AanmaakDatum", "WijzigingsDatum", "IsLocked") VALUES (5, '', '46a993a3-5172-4850-87e0-005bbda75828', '2023-04-13 00:00:00', '2023-04-13 00:00:00', false);


        --Multikanaal Mededelen (MKM)
        --ProjectId:	8235b51f-98b6-43a2-b854-07f1f705bccc
        --VersieId: 	124

        INSERT INTO "public"."Formulier" ("Id", "Nummer", "Status", "AanmaakDatum", "GebruikerId", "IndicatorLijstId", "WijzigingsDatum", "IsLocked")
        VALUES ('8235b51f-98b6-43a2-b854-07f1f705bccc', 0, 0, '2023-04-13 00:00:00', NULL, '64a37ba4-f636-423a-aa6f-85e5991baae0', '2023-04-13 00:00:00', false);

        INSERT INTO "public"."FormulierProjectVersie" ("FormulierenId", "ProjectVersiesId") VALUES ('8235b51f-98b6-43a2-b854-07f1f705bccc','124');

        INSERT INTO "public"."Antwoord" ("IndicatorId", "Waarde", "FormulierId", "AanmaakDatum", "WijzigingsDatum", "IsLocked") VALUES (99, '0.00', '8235b51f-98b6-43a2-b854-07f1f705bccc', '2023-04-13 00:00:00', '2023-04-13 00:00:00', false);
        INSERT INTO "public"."Antwoord" ("IndicatorId", "Waarde", "FormulierId", "AanmaakDatum", "WijzigingsDatum", "IsLocked") VALUES (98, '1.00', '8235b51f-98b6-43a2-b854-07f1f705bccc', '2023-04-13 00:00:00', '2023-04-13 00:00:00', false);
        INSERT INTO "public"."Antwoord" ("IndicatorId", "Waarde", "FormulierId", "AanmaakDatum", "WijzigingsDatum", "IsLocked") VALUES (5, 'Baten zijn kwalitatief en kwantitatief geraamd. De wijzigingen zullen vanaf 2018 een besparing in de ontwikkelkosten van mededelingen opleveren en de dienstverlening verbeteren. Ex ante wordt aangenomen dat de kosten om stromen toe te voegen op dit systeem in de eindsituatie ongeveer de helft goedkoper zijn dan in de huidige situatie. De aanpassingen moeten leiden tot besparingen in de (ontwikkel)kosten van mededelingen, het verkorten van de time-to-market en verbetering van de dienstverlening.', '8235b51f-98b6-43a2-b854-07f1f705bccc', '2023-04-13 00:00:00', '2023-04-13 00:00:00', false);

        INSERT INTO "__EFMigrationsHistory" ("MigrationId", "ProductVersion")
        VALUES ('20230416160135_AddMissendeBaten', '6.0.13');

        COMMIT;
    """
    op.execute(upgrade_query)
    op.execute("SET search_path TO public")


def downgrade() -> None:
    downgrade_query = """
        START TRANSACTION;

        DELETE FROM "public"."Formulier"
        WHERE ("public"."Formulier"."Id" = '90b08962-a412-4a80-b080-23f2f732a5a0')
        ;
        DELETE FROM "public"."Formulier"
        WHERE ("public"."Formulier"."Id" = '46a993a3-5172-4850-87e0-005bbda75828')
        ;
        DELETE FROM "public"."Formulier"
        WHERE ("public"."Formulier"."Id" = '8235b51f-98b6-43a2-b854-07f1f705bccc')
        ;

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = '1a62f45c-0c71-4abd-8651-3415e0052904', "SecurityStamp" = '174d9777-fb90-4d60-b216-ac19077bc505'
        WHERE "Id" = '258f96f3-ef86-4c00-b9f8-1cee593fd158';

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = '901d811a-9c41-4f1b-ad8b-c9880ed6a712', "SecurityStamp" = 'ac988702-0aa0-4601-bfcd-4161f71061f5'
        WHERE "Id" = '971c5b84-ce6f-4d8e-b009-c0fbc9ea452b';

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = 'cde311cf-0957-4096-b334-ae1ae55aa06e', "SecurityStamp" = '2d3724a7-caf8-4de4-b673-96b670d987d9'
        WHERE "Id" = '992dca13-29cf-491c-9b94-4462cd3bb3eb';

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = '0f9557fe-0efe-4a56-8289-f5e22edcdc34', "SecurityStamp" = '3abd214b-cd0a-4793-82d2-3be9083a8d32'
        WHERE "Id" = 'bc6eee82-2c77-4c19-9505-1f9a9a5cd0fa';

        UPDATE "AspNetUsers" SET "SecurityStamp" = 'fec32462-1fd4-4bf2-94fa-56072d154279'
        WHERE "Id" = 'f544b9a8-fd3d-480e-8966-413996ccfaa4';

        DELETE FROM "__EFMigrationsHistory"
        WHERE "MigrationId" = '20230416160135_AddMissendeBaten';

        COMMIT;


    """
    op.execute(downgrade_query)
    op.execute("SET search_path TO public")
