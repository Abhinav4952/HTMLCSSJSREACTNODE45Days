-- 01_schema.sql  (PostgreSQL 17)
--   psql -U course_user -d payflow -f database/01_schema.sql
-- The schema is OWNED by these scripts; Spring Boot runs with spring.jpa.hibernate.ddl-auto=validate.
-- Money columns use NUMERIC(19,4) - never floating point.

CREATE TABLE users (
    id            BIGSERIAL PRIMARY KEY,
    email         VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(100) NOT NULL,
    full_name     VARCHAR(120) NOT NULL,
    role          VARCHAR(10)  NOT NULL CHECK (role IN ('CUSTOMER', 'ADMIN')),
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT now()
);

CREATE TABLE accounts (
    id             BIGSERIAL PRIMARY KEY,
    owner_id       BIGINT         NOT NULL REFERENCES users (id),
    account_number VARCHAR(20)    NOT NULL UNIQUE,
    currency       CHAR(3)        NOT NULL,
    balance        NUMERIC(19, 4) NOT NULL DEFAULT 0 CHECK (balance >= 0),     -- no overdrafts
    status         VARCHAR(10)    NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'FROZEN', 'CLOSED')),
    version        BIGINT         NOT NULL DEFAULT 0,                          -- JPA @Version (optimistic locking)
    created_at     TIMESTAMPTZ    NOT NULL DEFAULT now()
);

CREATE TABLE transfers (
    id              BIGSERIAL PRIMARY KEY,
    from_account_id BIGINT         NOT NULL REFERENCES accounts (id),
    to_account_id   BIGINT         NOT NULL REFERENCES accounts (id),
    amount          NUMERIC(19, 4) NOT NULL CHECK (amount > 0),
    currency        CHAR(3)        NOT NULL,
    status          VARCHAR(10)    NOT NULL CHECK (status IN ('PENDING', 'COMPLETED', 'FAILED')),
    failure_reason  VARCHAR(255),
    created_at      TIMESTAMPTZ    NOT NULL DEFAULT now(),
    CONSTRAINT chk_transfer_distinct_accounts CHECK (from_account_id <> to_account_id)
);

-- Append-only double-entry style ledger. Rows are NEVER updated or deleted by the application.
CREATE TABLE ledger_entries (
    id            BIGSERIAL PRIMARY KEY,
    account_id    BIGINT         NOT NULL REFERENCES accounts (id),
    transfer_id   BIGINT         REFERENCES transfers (id),
    entry_type    VARCHAR(10)    NOT NULL CHECK (entry_type IN ('DEPOSIT', 'WITHDRAWAL', 'DEBIT', 'CREDIT')),
    amount        NUMERIC(19, 4) NOT NULL CHECK (amount > 0),
    balance_after NUMERIC(19, 4) NOT NULL CHECK (balance_after >= 0),
    description   VARCHAR(255),
    created_at    TIMESTAMPTZ    NOT NULL DEFAULT now()
);

-- One row per (user, Idempotency-Key header). A retry with the same key and same request returns the stored transfer.
CREATE TABLE idempotency_keys (
    user_id      BIGINT      NOT NULL REFERENCES users (id),
    idem_key     VARCHAR(64) NOT NULL,
    request_hash VARCHAR(64) NOT NULL,             -- SHA-256 of the request body; same key + different body => 422
    transfer_id  BIGINT      REFERENCES transfers (id),
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (user_id, idem_key)
);

CREATE INDEX idx_accounts_owner       ON accounts (owner_id);
CREATE INDEX idx_transfers_from       ON transfers (from_account_id, created_at);
CREATE INDEX idx_transfers_to         ON transfers (to_account_id, created_at);
CREATE INDEX idx_ledger_account_time  ON ledger_entries (account_id, created_at, id);
