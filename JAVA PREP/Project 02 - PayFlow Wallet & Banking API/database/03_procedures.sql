-- 03_procedures.sql
--   psql -U course_user -d payflow -f database/03_procedures.sql
--
-- fn_monthly_statement: a REAL PostgreSQL function stub for the monthly account statement.
-- It returns every ledger entry of one account in a calendar month (UTC) with a running balance that starts from the
-- balance at the end of the previous month. It already works; your assignment (Milestone E) is to
--   1. call it from Java (native query / JdbcTemplate / @NamedNativeQuery) behind GET /api/accounts/{id}/statements?year=&month=
--   2. add an opening-balance row and a closing-balance row (see the TODO below)
--   3. test it against PostgreSQL (the course's H2 tests cannot run PL/pgSQL).
--
-- Usage:  SELECT * FROM fn_monthly_statement(1, 2025, 3);

CREATE OR REPLACE FUNCTION fn_monthly_statement(p_account_id BIGINT, p_year INT, p_month INT)
RETURNS TABLE (
    entry_id        BIGINT,
    posted_at       TIMESTAMPTZ,
    entry_type      VARCHAR,
    description     VARCHAR,
    debit           NUMERIC,
    credit          NUMERIC,
    running_balance NUMERIC
)
LANGUAGE plpgsql
STABLE
AS $$
DECLARE
    v_start   TIMESTAMPTZ;
    v_end     TIMESTAMPTZ;
    v_opening NUMERIC(19, 4);
BEGIN
    IF p_month < 1 OR p_month > 12 THEN
        RAISE EXCEPTION 'invalid month: %', p_month USING ERRCODE = '22023';
    END IF;

    v_start := make_timestamptz(p_year, p_month, 1, 0, 0, 0, 'UTC');
    v_end   := v_start + INTERVAL '1 month';

    -- Balance carried over from before the month: credits/deposits add, debits/withdrawals subtract.
    SELECT COALESCE(SUM(CASE WHEN le.entry_type IN ('DEPOSIT', 'CREDIT') THEN le.amount ELSE -le.amount END), 0)
      INTO v_opening
      FROM ledger_entries le
     WHERE le.account_id = p_account_id
       AND le.created_at < v_start;

    RETURN QUERY
    SELECT le.id,
           le.created_at,
           le.entry_type::VARCHAR,
           le.description::VARCHAR,
           (CASE WHEN le.entry_type IN ('DEBIT', 'WITHDRAWAL') THEN le.amount ELSE 0 END)::NUMERIC,
           (CASE WHEN le.entry_type IN ('DEPOSIT', 'CREDIT')   THEN le.amount ELSE 0 END)::NUMERIC,
           (v_opening + SUM(CASE WHEN le.entry_type IN ('DEPOSIT', 'CREDIT') THEN le.amount ELSE -le.amount END)
                        OVER (ORDER BY le.created_at, le.id))::NUMERIC
      FROM ledger_entries le
     WHERE le.account_id = p_account_id
       AND le.created_at >= v_start
       AND le.created_at <  v_end
     ORDER BY le.created_at, le.id;

    -- TODO(Project 02, Milestone E): also return an "OPENING" row (v_opening) first and a "CLOSING" row last,
    --                                and decide what to return for an account that does not exist.
END;
$$;
