-- 00_create_database.sql
-- Run as a PostgreSQL superuser, connected to the default `postgres` database:
--   psql -U postgres -f database/00_create_database.sql
-- Safe to run more than once.

DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'course_user') THEN
        CREATE ROLE course_user WITH LOGIN PASSWORD 'change_me';
    END IF;
END
$$;

-- CREATE DATABASE cannot run inside a DO block; \gexec (psql) executes the generated statement only when needed.
SELECT 'CREATE DATABASE payflow OWNER course_user'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'payflow')\gexec

GRANT ALL PRIVILEGES ON DATABASE payflow TO course_user;
