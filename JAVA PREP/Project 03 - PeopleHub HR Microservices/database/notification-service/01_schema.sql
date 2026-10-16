-- 01_schema.sql (peoplehub_notification)
--   psql -U course_user -d peoplehub_notification -f database/notification-service/01_schema.sql
-- Owner of: notifications and the idempotency table of the Kafka consumer.

CREATE TABLE notifications (
    id                    BIGSERIAL PRIMARY KEY,
    recipient_employee_id BIGINT       NOT NULL,                -- id in employee-service (no cross-database FK)
    type                  VARCHAR(30)  NOT NULL,                -- e.g. LEAVE_APPROVED
    message               VARCHAR(500) NOT NULL,
    status                VARCHAR(10)  NOT NULL DEFAULT 'NEW' CHECK (status IN ('NEW', 'SENT', 'READ')),
    source_event_id       VARCHAR(64),
    created_at            TIMESTAMPTZ  NOT NULL DEFAULT now()
);

-- Idempotent consumer: the primary key rejects a second delivery of the same event.
CREATE TABLE processed_events (
    event_id     VARCHAR(64) PRIMARY KEY,
    processed_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_notifications_recipient ON notifications (recipient_employee_id, created_at DESC);
