-- 99_reset.sql (peoplehub_notification)  DESTRUCTIVE
--   psql -U course_user -d peoplehub_notification -f database/<service>/99_reset.sql
-- Then re-run 01_schema.sql and 02_seed_data.sql.

DROP TABLE IF EXISTS processed_events CASCADE;
DROP TABLE IF EXISTS notifications CASCADE;
