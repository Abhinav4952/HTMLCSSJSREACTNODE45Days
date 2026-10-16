-- PROVIDED (do not edit)
CREATE TABLE accounts (
    id            BIGINT PRIMARY KEY,
    owner         VARCHAR(50) NOT NULL,
    balance_cents BIGINT NOT NULL CHECK (balance_cents >= 0),
    status        VARCHAR(10) NOT NULL DEFAULT 'ACTIVE'
);
