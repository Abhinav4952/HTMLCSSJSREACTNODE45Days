-- 03_procedures.sql  (PLACEHOLDER)
-- Reserved for optional database-side logic. The main implementation lives in Java (service layer); use this file only
-- if your team decides that a rule is better enforced or reported inside PostgreSQL (e.g. occupancy reports).
-- Run after 01_schema.sql:  psql -U course_user -d stayeasy -f database/03_procedures.sql

-- Example helper you may call from a native query: is the room free for [p_check_in, p_check_out) ?
CREATE OR REPLACE FUNCTION fn_is_room_available(p_room_id BIGINT, p_check_in DATE, p_check_out DATE)
RETURNS BOOLEAN
LANGUAGE sql
STABLE
AS $$
    SELECT NOT EXISTS (
        SELECT 1
        FROM bookings b
        WHERE b.room_id = p_room_id
          AND b.status IN ('PENDING', 'CONFIRMED')
          AND daterange(b.check_in, b.check_out, '[)') && daterange(p_check_in, p_check_out, '[)')
    );
$$;

-- TODO (optional stretch): fn_occupancy_report(p_hotel_id BIGINT, p_from DATE, p_to DATE) returning booked nights per room.
