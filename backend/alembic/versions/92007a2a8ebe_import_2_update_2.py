"""import 2 update 2

Revsion ID: 92007a2a8ebe
Revises: b49569d3f0cf
Create Date: 2023-02-15 15:45:00

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "92007a2a8ebe"
down_revision = "b49569d3f0cf"
branch_labels = None
depends_on = None


def upgrade() -> None:
    upgrade_query = """

        START TRANSACTION;

        ALTER TABLE "IndicatorLijst" ADD "Vereist" boolean NOT NULL DEFAULT FALSE;

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

        INSERT INTO "__EFMigrationsHistory" ("MigrationId", "ProductVersion")
        VALUES ('20230216133725_AddVereistToIndicatorlijst', '6.0.13');

        UPDATE "public"."Antwoord"
        SET "IndicatorId"='85'
        WHERE ("Antwoord"."IndicatorId" = 64)
        AND "Antwoord"."FormulierId" IN 
        (
            SELECT distinct "FormulierId"
            FROM "public"."Antwoord"
            WHERE "Antwoord"."IndicatorId" = 71
        );

        UPDATE "public"."Antwoord"
        SET "IndicatorId"='87'
        WHERE ("Antwoord"."IndicatorId" = 66)
        AND "Antwoord"."FormulierId" IN 
        (
            SELECT distinct "FormulierId"
            FROM "public"."Antwoord"
            WHERE "Antwoord"."IndicatorId" = 71
        );

        UPDATE "public"."Antwoord" SET "Waarde" = TRIM("Waarde")
        ;
        UPDATE "public"."AntwoordOptie" SET "Waarde" = TRIM("Waarde")
        ;

        UPDATE "public"."Indicator" SET "Titel" = upper(substring("Titel" from 1 for 1)) || lower(substring("Titel" from 2 for length("Titel")))
        ;
        UPDATE "public"."Indicator"
        SET "Titel"='BIT-Toets'
        WHERE ("public"."Indicator"."Id" = 97)
        ;
        UPDATE "public"."Indicator"
        SET "Toelichting"='Bedragen in miljoenen - Intern Personeel: Kosten personeel werkzaam aan de ICT-activiteit. Voor ‘eigen’ personeel worden de geschatte en gerealiseerde uitgaven gerapporteerd op basis van het in het (bijgewerkte) projectplan (of vergelijkbaar) begrote en geschatte aantal dagen. - Extern personeel: Inhuur van externe personele capaciteit van externe bedrijven ten behoeve van ICT-taken. - Overig materiaal: Dit is een samenvoeging van wat voorheen hardware, standaardsoftware en dataverbindingen was. Deze kunnen opgeteld worden.'
        WHERE ("public"."Indicator"."Id" = 62)
        ;
        UPDATE "public"."Indicator"
        SET "Vereist"='false', "Toelichting"='Welk systeem van toerekening is gehanteerd? Besteed aandacht aan: - Het hanteren van het kasverplichtingen-  of baten-lastenstelsel; - De wijze van toerekenen van kosten van intern personeel; - Exploitatiekosten die, ten tijde van de uitvoering, nog als kosten van de ICT-activitei worden meegenomen.'
        WHERE ("public"."Indicator"."Id" = 4)
        ;
        UPDATE "public"."Indicator"
        SET "Vereist"='false', "Toelichting"='Als in de businesscase geen (economische) levensduur van het resultaat is gecalculeerd wordt dat hier toegelicht.'
        WHERE ("public"."Indicator"."Id" = 3)
        ;
        UPDATE "public"."Indicator"
        SET "Toelichting"='IT-deel decharge. Bij een beheer en onderhoud traject: gebruik eind levensduur.'
        WHERE ("public"."Indicator"."Id" = 20)
        ;

        UPDATE "public"."IndicatorLijst"
        SET "Vereist"='true'
        WHERE ("public"."IndicatorLijst"."Id" = '5647e13f-427e-482b-b2c7-b0975766daa6')
        ;
        UPDATE "public"."IndicatorLijst"
        SET "Vereist"='true'
        WHERE ("public"."IndicatorLijst"."Id" = '2997e04a-5d85-40ac-afb8-690016c124e3')
        ;
        UPDATE "public"."IndicatorLijst"
        SET "Vereist"='true'
        WHERE ("public"."IndicatorLijst"."Id" = 'a424c56c-e3e0-451a-bd0c-4f1c2d2108f3')
        ;

        COMMIT;

    """
    op.execute(upgrade_query)


def downgrade() -> None:
    downgrade_query = """
    
        START TRANSACTION;

        ALTER TABLE "IndicatorLijst" DROP COLUMN "Vereist";

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = '7285f113-6aa7-40b2-8060-032a619de587', "SecurityStamp" = '08705f01-0479-4d73-a2e0-a3704c047b2a'
        WHERE "Id" = '258f96f3-ef86-4c00-b9f8-1cee593fd158';

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = '3a844287-b328-4e09-965e-f64664871cee', "SecurityStamp" = '1ea4d7f2-d207-4816-ad48-b2ef272e8f60'
        WHERE "Id" = '971c5b84-ce6f-4d8e-b009-c0fbc9ea452b';

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = 'ae807691-f514-4e29-bbaa-3c0ab482aa90', "SecurityStamp" = '16d5d57e-aa98-4b49-ac16-855037d14b89'
        WHERE "Id" = '992dca13-29cf-491c-9b94-4462cd3bb3eb';

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = '8db51e9a-0b7a-45ee-99bb-db47a41f7a55', "SecurityStamp" = '8ade73b8-774a-4c93-9cfa-3aef60b6313c'
        WHERE "Id" = 'bc6eee82-2c77-4c19-9505-1f9a9a5cd0fa';

        UPDATE "AspNetUsers" SET "SecurityStamp" = 'a37d16aa-2d4b-4060-a0cb-61cc7128a94d'
        WHERE "Id" = 'f544b9a8-fd3d-480e-8966-413996ccfaa4';

        DELETE FROM "__EFMigrationsHistory"
        WHERE "MigrationId" = '20230216133725_AddVereistToIndicatorlijst';

        COMMIT;

    """
    op.execute(downgrade_query)
