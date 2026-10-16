-- 99_reset.sql (peoplehub_leave)  DESTRUCTIVE
--   psql -U course_user -d peoplehub_leave -f database/<service>/99_reset.sql
-- Then re-run 01_schema.sql and 02_seed_data.sql.

DROP TABLE IF EXISTS outbox_events CASCADE;
DROP TABLE IF EXISTS leave_balances CASCADE;
DROP TABLE IF EXISTS leave_requests CASCADE;
