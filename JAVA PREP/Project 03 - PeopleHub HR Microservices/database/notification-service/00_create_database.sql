-- 00_create_database.sql  (peoplehub_notification)
-- Run as a PostgreSQL superuser connected to the default `postgres` database:
--   psql -U postgres -f database/peoplehub_notification/00_create_database.sql
-- Safe to run more than once. Each service owns its OWN database - there are no cross-database foreign keys.

DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'course_user') THEN
        CREATE ROLE course_user WITH LOGIN PASSWORD 'change_me';
    END IF;
END
$$;

SELECT 'CREATE DATABASE peoplehub_notification OWNER course_user'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'peoplehub_notification')\gexec

GRANT ALL PRIVILEGES ON DATABASE peoplehub_notification TO course_user;
