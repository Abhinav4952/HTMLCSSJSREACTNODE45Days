-- 01_schema.sql (peoplehub_leave)
--   psql -U course_user -d peoplehub_leave -f database/leave-service/01_schema.sql
-- Owner of: leave requests, yearly balances and the OUTBOX of domain events.
-- employee_id / approver_id are plain BIGINT values referencing employee-service ids: NO foreign key across databases.
-- Validate them through the employee-service API (RestClient) instead.

CREATE TABLE leave_requests (
    id          BIGSERIAL PRIMARY KEY,
    employee_id BIGINT      NOT NULL,
    approver_id BIGINT,
    leave_type  VARCHAR(10) NOT NULL CHECK (leave_type IN ('ANNUAL', 'SICK', 'UNPAID')),
    start_date  DATE        NOT NULL,
    end_date    DATE        NOT NULL,
    days        INT         NOT NULL CHECK (days > 0),
    status      VARCHAR(10) NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'APPROVED', 'REJECTED', 'CANCELLED')),
    reason      VARCHAR(500),
    decided_at  TIMESTAMPTZ,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_leave_dates CHECK (end_date >= start_date),
    CONSTRAINT chk_decision CHECK ((status IN ('APPROVED', 'REJECTED') AND approver_id IS NOT NULL AND decided_at IS NOT NULL)
                                   OR status IN ('PENDING', 'CANCELLED'))
);

CREATE TABLE leave_balances (
    employee_id BIGINT NOT NULL,
    year        INT    NOT NULL,
    total_days  INT    NOT NULL CHECK (total_days >= 0),
    used_days   INT    NOT NULL DEFAULT 0 CHECK (used_days >= 0),
    PRIMARY KEY (employee_id, year),
    CONSTRAINT chk_used_within_total CHECK (used_days <= total_days)
);

-- Transactional outbox: written in the SAME transaction as the approval, relayed to Kafka by a poller (Day 46).
CREATE TABLE outbox_events (
    id             BIGSERIAL PRIMARY KEY,
    aggregate_type VARCHAR(50)  NOT NULL,
    aggregate_id   VARCHAR(50)  NOT NULL,
    event_type     VARCHAR(50)  NOT NULL,
    topic          VARCHAR(100) NOT NULL,
    event_key      VARCHAR(50)  NOT NULL,
    payload        JSONB        NOT NULL,
    published      BOOLEAN      NOT NULL DEFAULT FALSE,
    created_at     TIMESTAMPTZ  NOT NULL DEFAULT now(),
    published_at   TIMESTAMPTZ
);

CREATE INDEX idx_leave_employee          ON leave_requests (employee_id, start_date);
CREATE INDEX idx_leave_status            ON leave_requests (status);
CREATE INDEX idx_outbox_unpublished      ON outbox_events (id) WHERE published = FALSE;
