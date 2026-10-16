-- 99_reset.sql (peoplehub_employee)  DESTRUCTIVE
--   psql -U course_user -d peoplehub_employee -f database/<service>/99_reset.sql
-- Then re-run 01_schema.sql and 02_seed_data.sql.

DROP TABLE IF EXISTS employees CASCADE;
DROP TABLE IF EXISTS departments CASCADE;
