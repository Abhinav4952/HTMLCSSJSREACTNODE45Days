-- 02_seed_data.sql (peoplehub_notification)
INSERT INTO notifications (recipient_employee_id, type, message, status, source_event_id) VALUES
 (3, 'LEAVE_APPROVED', 'Your annual leave request #1 (5 days) was approved by Milo Grant.', 'READ', 'seed-event-0001');
INSERT INTO processed_events (event_id) VALUES ('seed-event-0001');
