"""add started to project

Revision ID: f56256f4f19f
Revises: ef2d755b1e58
Create Date: 2023-04-16 20:05:00

upgrade script command:
script-migration Datamigratie3Update1 AddLockedToVersieAndStartedToProject

downgrade script command:
script-migration AddLockedToVersieAndStartedToProject Datamigratie3Update1

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "f56256f4f19f"
down_revision = "ef2d755b1e58"
branch_labels = None
depends_on = None


def upgrade() -> None:
    upgrade_query = """
        START TRANSACTION;

        ALTER TABLE "ProjectVersie" ADD "IsLocked" boolean NOT NULL DEFAULT FALSE;

        ALTER TABLE "Project" ADD "IsGestart" boolean NOT NULL DEFAULT FALSE;

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

        UPDATE "public"."Project"
        SET "IsGestart"='true'
        WHERE ("public"."Project"."Nummer" NOT IN ('639276','1313607'))
        ;

        INSERT INTO "__EFMigrationsHistory" ("MigrationId", "ProductVersion")
        VALUES ('20230416123523_AddLockedToVersieAndStartedToProject', '6.0.13');

        COMMIT;
    """
    op.execute(upgrade_query)
    op.execute("SET search_path TO public")


def downgrade() -> None:
    downgrade_query = """
        START TRANSACTION;

        ALTER TABLE "ProjectVersie" DROP COLUMN "IsLocked";

        ALTER TABLE "Project" DROP COLUMN "IsGestart" Cascade;

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

        DELETE FROM "__EFMigrationsHistory"
        WHERE "MigrationId" = '20230416123523_AddLockedToVersieAndStartedToProject';

        COMMIT;

    """
    op.execute(downgrade_query)
    op.execute("SET search_path TO public")
