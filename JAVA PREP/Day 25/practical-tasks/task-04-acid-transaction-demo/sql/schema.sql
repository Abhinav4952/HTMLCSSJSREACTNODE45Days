-- PROVIDED (do not edit)
CREATE TABLE accounts (
    id            BIGINT PRIMARY KEY,
    owner         VARCHAR(50) NOT NULL UNIQUE,
    balance_cents BIGINT NOT NULL CHECK (balance_cents >= 0)
);
