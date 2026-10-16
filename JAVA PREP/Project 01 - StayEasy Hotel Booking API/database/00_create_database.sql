-- 00_create_database.sql
-- Run as a PostgreSQL superuser (usually `postgres`), connected to the default `postgres` database:
--   psql -U postgres -f database/00_create_database.sql
-- Safe to run more than once.

DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'course_user') THEN
        CREATE ROLE course_user WITH LOGIN PASSWORD 'change_me';
    END IF;
END
$$;

-- CREATE DATABASE cannot run inside a DO block; \gexec runs the generated statement only when needed (psql feature).
SELECT 'CREATE DATABASE stayeasy OWNER course_user'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'stayeasy')\gexec

GRANT ALL PRIVILEGES ON DATABASE stayeasy TO course_user;
