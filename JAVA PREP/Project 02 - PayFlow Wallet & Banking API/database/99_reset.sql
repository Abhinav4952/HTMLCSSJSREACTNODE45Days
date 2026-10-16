-- 99_reset.sql  (DESTRUCTIVE)
--   psql -U course_user -d payflow -f database/99_reset.sql
-- Then re-run 01_schema.sql, 02_seed_data.sql, 03_procedures.sql.

DROP FUNCTION IF EXISTS fn_monthly_statement(BIGINT, INT, INT);
DROP TABLE IF EXISTS idempotency_keys CASCADE;
DROP TABLE IF EXISTS ledger_entries   CASCADE;
DROP TABLE IF EXISTS transfers        CASCADE;
DROP TABLE IF EXISTS accounts         CASCADE;
DROP TABLE IF EXISTS users            CASCADE;
