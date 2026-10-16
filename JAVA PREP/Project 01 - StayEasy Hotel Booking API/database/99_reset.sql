-- 99_reset.sql
-- DESTRUCTIVE: drops every StayEasy object so you can start over.
--   psql -U course_user -d stayeasy -f database/99_reset.sql
-- Then re-run 01_schema.sql, 02_seed_data.sql and (optionally) 03_procedures.sql.

DROP FUNCTION IF EXISTS fn_is_room_available(BIGINT, DATE, DATE);
DROP TABLE IF EXISTS bookings CASCADE;
DROP TABLE IF EXISTS rooms    CASCADE;
DROP TABLE IF EXISTS hotels   CASCADE;
DROP TABLE IF EXISTS users    CASCADE;
