-- Adminer 4.8.1 PostgreSQL 14.4 (Debian 14.4-1.pgdg110+1) dump

\connect "postgres";

DROP TABLE IF EXISTS "test";
DROP SEQUENCE IF EXISTS test_id_seq;
CREATE SEQUENCE test_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."test" (
    "id" integer DEFAULT nextval('test_id_seq') NOT NULL,
    "sometext" character varying(255) NOT NULL,
    "time" timestamp NOT NULL,
    CONSTRAINT "test_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


-- 2022-06-27 12:07:23.053231+00
