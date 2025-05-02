"""datamigratie 3 update 1

Revision ID: e9ee3b3842ab
Revises: 72655ee53692
Create Date: 2023-04-07 17:39:00

upgrade
script-migration UpdateOrganisaties Datamigratie3Update1
downgrade
script-migration Datamigratie3Update1 UpdateOrganisaties

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "e9ee3b3842ab"
down_revision = "72655ee53692"
branch_labels = None
depends_on = None


def upgrade() -> None:
    upgrade_query = """

        START TRANSACTION;

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = '409aed6c-9295-4386-bb6a-ec9b16d98dc0', "SecurityStamp" = 'a357a1ac-dc06-4ebc-9d7d-a271b7ffb297'
        WHERE "Id" = '258f96f3-ef86-4c00-b9f8-1cee593fd158';

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = '7fe71230-9e6f-4225-ad3d-c1660a57b9bf', "SecurityStamp" = '8b0a29ae-f02a-4de4-9e7c-22dd1bc97a01'
        WHERE "Id" = '971c5b84-ce6f-4d8e-b009-c0fbc9ea452b';

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = '7438ba8e-e589-4663-ab15-bbae8f7470f9', "SecurityStamp" = '6eb92cfd-983a-4879-9f59-89c437dd36d9'
        WHERE "Id" = '992dca13-29cf-491c-9b94-4462cd3bb3eb';

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = '204e1cd7-7b8d-4b20-a290-4a4643cfea83', "SecurityStamp" = 'ab9aa8f8-0f34-4eb2-a69e-334c2ddaccb7'
        WHERE "Id" = 'bc6eee82-2c77-4c19-9505-1f9a9a5cd0fa';

        UPDATE "AspNetUsers" SET "SecurityStamp" = '911ad558-fb0b-404a-b09a-07ec72cd0b9f'
        WHERE "Id" = 'f544b9a8-fd3d-480e-8966-413996ccfaa4';

        UPDATE "public"."Antwoord"
        SET "Waarde"='Economie;Recht, veiligheid en defensie'
        WHERE ("public"."Antwoord"."Id" = 55916)
        ;
        UPDATE "public"."Antwoord"
        SET "Waarde"='Migratie en reizen;Overheid en democratie'
        WHERE ("public"."Antwoord"."Id" = 69603)
        ;
        UPDATE "public"."Antwoord"
        SET "Waarde"='Recht, veiligheid en defensie;Migratie en reizen'
        WHERE ("public"."Antwoord"."Id" = 65505)
        ;
        UPDATE "public"."Antwoord"
        SET "Waarde"='Internationale samenwerking;Recht, veiligheid en defensie'
        WHERE ("public"."Antwoord"."Id" = 63403)
        ;

        INSERT INTO "__EFMigrationsHistory" ("MigrationId", "ProductVersion")
        VALUES ('20230407154101_Datamigratie3Update1', '6.0.13');

        COMMIT;
        
    """
    op.execute(upgrade_query)
    op.execute("SET search_path TO public")


def downgrade() -> None:
    downgrade_query = """

        START TRANSACTION;

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = '053486b3-c0b0-4dc9-8d1d-19ff023126ce', "SecurityStamp" = '2c8186fc-067a-4d68-8064-2d0b55de0b3a'
        WHERE "Id" = '258f96f3-ef86-4c00-b9f8-1cee593fd158';

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = '4cc3ac38-6b73-4b02-9b3e-d49943fc32da', "SecurityStamp" = 'be76e90f-0c43-4fa1-bbc4-f09db7ae40c4'
        WHERE "Id" = '971c5b84-ce6f-4d8e-b009-c0fbc9ea452b';

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = '8d590628-f444-4bc1-bb9b-66090b3e80f6', "SecurityStamp" = '3bb871d9-48c2-496f-997e-a37f52d65cb4'
        WHERE "Id" = '992dca13-29cf-491c-9b94-4462cd3bb3eb';

        UPDATE "AspNetUsers" SET "ConcurrencyStamp" = '2fc033d7-fa1e-4a63-b3ea-6b93de2dd53d', "SecurityStamp" = '68520366-cde8-4024-b5f3-2b3fe36dcf7d'
        WHERE "Id" = 'bc6eee82-2c77-4c19-9505-1f9a9a5cd0fa';

        UPDATE "AspNetUsers" SET "SecurityStamp" = '298b654f-dd1c-49dc-9892-3673b1fd3f7c'
        WHERE "Id" = 'f544b9a8-fd3d-480e-8966-413996ccfaa4';

        DELETE FROM "__EFMigrationsHistory"
        WHERE "MigrationId" = '20230407154101_Datamigratie3Update1';

        COMMIT;
        
    """
    op.execute(downgrade_query)
    op.execute("SET search_path TO public")
