PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE "django_site" (
    "id" integer NOT NULL PRIMARY KEY,
    "domain" varchar(100) NOT NULL,
    "name" varchar(50) NOT NULL
);
DELETE FROM "django_site" WHERE "id" != 0;
INSERT INTO "django_site" VALUES(1,'localhost:7000','Dev Domain');
COMMIT;
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE "socialaccount_socialapp" (
    "id" integer NOT NULL PRIMARY KEY,
    "provider" varchar(30) NOT NULL,
    "name" varchar(40) NOT NULL,
    "client_id" varchar(100) NOT NULL,
    "key" varchar(100) NOT NULL,
    "secret" varchar(100) NOT NULL
);
DELETE FROM "socialaccount_socialapp" WHERE "id" != 0;
INSERT INTO "socialaccount_socialapp" VALUES(3,'twitter','Twitter login','a4PAin0cDtFQ2ig1egl0A','','FuRAGOhUAjaNBioOmkXEg3vEygpSAUzxcXyNsU8d4Y');
INSERT INTO "socialaccount_socialapp" VALUES(4,'linkedin','LinkedIn login','77dmfxvujdlsh0','','rz0NtfmFizNOqpMM');
INSERT INTO "socialaccount_socialapp" VALUES(6,'google','Google+ login','428825681483.apps.googleusercontent.com','','rzdIFZSWZXslUuUOvU15Ai4x');
INSERT INTO "socialaccount_socialapp" VALUES(8,'facebook','FB login','179432562251645','','c1e40064e4db7c6817b221b04405e1c6');
COMMIT;
CREATE TABLE "socialaccount_socialapp_sites" (
    "id" integer NOT NULL PRIMARY KEY,
    "socialapp_id" integer NOT NULL,
    "site_id" integer NOT NULL REFERENCES "django_site" ("id"),
    UNIQUE ("socialapp_id", "site_id")
);
DELETE FROM "socialaccount_socialapp_sites" WHERE "id" != 0;
INSERT INTO "socialaccount_socialapp_sites" VALUES(12,8,1);
INSERT INTO "socialaccount_socialapp_sites" VALUES(13,6,1);
INSERT INTO "socialaccount_socialapp_sites" VALUES(14,4,1);
INSERT INTO "socialaccount_socialapp_sites" VALUES(15,3,1);
CREATE INDEX "socialaccount_socialapp_sites_f2973cd1" ON "socialaccount_socialapp_sites" ("socialapp_id");
CREATE INDEX "socialaccount_socialapp_sites_99732b5c" ON "socialaccount_socialapp_sites" ("site_id");
COMMIT;
