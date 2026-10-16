-- 00_create_database.sql  (peoplehub_employee)
-- Run as a PostgreSQL superuser connected to the default `postgres` database:
--   psql -U postgres -f database/peoplehub_employee/00_create_database.sql
-- Safe to run more than once. Each service owns its OWN database - there are no cross-database foreign keys.

DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'course_user') THEN
        CREATE ROLE course_user WITH LOGIN PASSWORD 'change_me';
    END IF;
END
$$;

SELECT 'CREATE DATABASE peoplehub_employee OWNER course_user'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'peoplehub_employee')\gexec

GRANT ALL PRIVILEGES ON DATABASE peoplehub_employee TO course_user;
