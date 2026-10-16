-- 02_seed_data.sql (peoplehub_leave)
-- employee ids refer to peoplehub_employee (1 = HR, 2 = manager Milo, 3 = Alice, 4 = Bob, 5 = Carol).

INSERT INTO leave_balances (employee_id, year, total_days, used_days) VALUES
 (2, EXTRACT(YEAR FROM CURRENT_DATE)::int, 20, 0),
 (3, EXTRACT(YEAR FROM CURRENT_DATE)::int, 20, 5),
 (4, EXTRACT(YEAR FROM CURRENT_DATE)::int, 20, 0),
 (5, EXTRACT(YEAR FROM CURRENT_DATE)::int, 20, 0);

INSERT INTO leave_requests (id, employee_id, approver_id, leave_type, start_date, end_date, days, status, reason, decided_at) VALUES
 (1, 3, 2,    'ANNUAL', CURRENT_DATE - 30, CURRENT_DATE - 26, 5, 'APPROVED',  'Family trip',   now() - INTERVAL '35 days'),
 (2, 4, NULL, 'ANNUAL', CURRENT_DATE + 14, CURRENT_DATE + 16, 3, 'PENDING',   'Long weekend',  NULL),
 (3, 5, NULL, 'SICK',   CURRENT_DATE + 1,  CURRENT_DATE + 1,  1, 'PENDING',   'Doctor visit',  NULL),
 (4, 3, 2,    'UNPAID', CURRENT_DATE + 40, CURRENT_DATE + 44, 5, 'REJECTED',  'Sabbatical',    now() - INTERVAL '2 days');

SELECT setval(pg_get_serial_sequence('leave_requests', 'id'), (SELECT MAX(id) FROM leave_requests));

-- The already-approved request 1 has a matching outbox row so you can test your poller immediately.
INSERT INTO outbox_events (aggregate_type, aggregate_id, event_type, topic, event_key, payload, published) VALUES
 ('LeaveRequest', '1', 'LeaveApproved', 'leave.approved.v1', '3',
  '{"version":1,"eventId":"seed-event-0001","leaveRequestId":1,"employeeId":3,"approverId":2,"leaveType":"ANNUAL","days":5}'::jsonb, FALSE);
