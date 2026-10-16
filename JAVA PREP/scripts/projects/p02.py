"""Project 02 - PayFlow Wallet & Banking API."""
from pathlib import Path

from skeleton import sub, write, write_service

NAME = "Project 02 - PayFlow Wallet & Banking API"
DB = "payflow"

HASH = {
    "admin": "$2a$10$6Ai9fZGYXWcJcFj2FxED0eBQ5dBwrOgfgQg/1dRO.Cq6F4VT/ku2C",   # Admin@123
    "alice": "$2a$10$E1CeAbXchPDULuJ31jx1.OUSr7ffnPs0arczbvZc8ZbGU7qCUZkOG",   # Alice@123
    "bob": "$2a$10$OfLP3.Q9SjzEDOi5GU4wFeSE.0KkVV.WyJutnnTcKa8UCOFjiEimC",     # Bob@123
}

CREATE_DB = """-- 00_create_database.sql
-- Run as a PostgreSQL superuser, connected to the default `postgres` database:
--   psql -U postgres -f database/00_create_database.sql
-- Safe to run more than once.

DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'course_user') THEN
        CREATE ROLE course_user WITH LOGIN PASSWORD 'change_me';
    END IF;
END
$$;

-- CREATE DATABASE cannot run inside a DO block; \\gexec (psql) executes the generated statement only when needed.
SELECT 'CREATE DATABASE payflow OWNER course_user'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'payflow')\\gexec

GRANT ALL PRIVILEGES ON DATABASE payflow TO course_user;
"""

SCHEMA = """-- 01_schema.sql  (PostgreSQL 17)
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
"""

SEED = """-- 02_seed_data.sql
--   psql -U course_user -d payflow -f database/02_seed_data.sql
-- Seed logins (plain-text passwords are documented in README.md; only BCrypt hashes are stored):
--   admin@payflow.com / Admin@123      alice@payflow.com / Alice@123      bob@payflow.com / Bob@123
--
-- Ledger and balances are consistent: balance_after of the last entry == accounts.balance.
-- Entry timestamps are relative to the start of the current month so fn_monthly_statement has data for last month and this month.

INSERT INTO users (id, email, password_hash, full_name, role) VALUES
 (1, 'admin@payflow.com', '@@ADMIN@@', 'Ada Admin',  'ADMIN'),
 (2, 'alice@payflow.com', '@@ALICE@@', 'Alice Smith', 'CUSTOMER'),
 (3, 'bob@payflow.com',   '@@BOB@@',   'Bob Jones',   'CUSTOMER');

INSERT INTO accounts (id, owner_id, account_number, currency, balance, status) VALUES
 (1, 2, 'PF-1000-0001', 'USD', 1300.0000, 'ACTIVE'),   -- Alice checking: 1000 + 500 - 200
 (2, 3, 'PF-1000-0002', 'USD',  500.0000, 'ACTIVE'),   -- Bob checking:   300 + 200
 (3, 2, 'PF-1000-0003', 'USD', 2000.0000, 'ACTIVE'),   -- Alice savings
 (4, 3, 'PF-1000-0004', 'USD',    0.0000, 'FROZEN');   -- Bob frozen account (tests rejecting transfers)

INSERT INTO transfers (id, from_account_id, to_account_id, amount, currency, status, created_at) VALUES
 (1, 1, 2, 200.0000, 'USD', 'COMPLETED', date_trunc('month', now()) + INTERVAL '2 days');

INSERT INTO idempotency_keys (user_id, idem_key, request_hash, transfer_id) VALUES
 (2, 'seed-transfer-0001', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 1);

INSERT INTO ledger_entries (account_id, transfer_id, entry_type, amount, balance_after, description, created_at) VALUES
 (1, NULL, 'DEPOSIT', 1000.0000, 1000.0000, 'Initial deposit',  date_trunc('month', now()) - INTERVAL '25 days'),
 (1, NULL, 'DEPOSIT',  500.0000, 1500.0000, 'Salary',           date_trunc('month', now()) - INTERVAL '5 days'),
 (1, 1,    'DEBIT',    200.0000, 1300.0000, 'Transfer to Bob',  date_trunc('month', now()) + INTERVAL '2 days'),
 (2, NULL, 'DEPOSIT',  300.0000,  300.0000, 'Initial deposit',  date_trunc('month', now()) - INTERVAL '20 days'),
 (2, 1,    'CREDIT',   200.0000,  500.0000, 'Transfer from Alice', date_trunc('month', now()) + INTERVAL '2 days'),
 (3, NULL, 'DEPOSIT', 2000.0000, 2000.0000, 'Savings opening',  date_trunc('month', now()) - INTERVAL '15 days');

SELECT setval(pg_get_serial_sequence('users', 'id'),     (SELECT MAX(id) FROM users));
SELECT setval(pg_get_serial_sequence('accounts', 'id'),  (SELECT MAX(id) FROM accounts));
SELECT setval(pg_get_serial_sequence('transfers', 'id'), (SELECT MAX(id) FROM transfers));
"""

PROC = """-- 03_procedures.sql
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
"""

RESET = """-- 99_reset.sql  (DESTRUCTIVE)
--   psql -U course_user -d payflow -f database/99_reset.sql
-- Then re-run 01_schema.sql, 02_seed_data.sql, 03_procedures.sql.

DROP FUNCTION IF EXISTS fn_monthly_statement(BIGINT, INT, INT);
DROP TABLE IF EXISTS idempotency_keys CASCADE;
DROP TABLE IF EXISTS ledger_entries   CASCADE;
DROP TABLE IF EXISTS transfers        CASCADE;
DROP TABLE IF EXISTS accounts         CASCADE;
DROP TABLE IF EXISTS users            CASCADE;
"""

DB_SETUP = """# PayFlow - Database Setup (PostgreSQL 17)

Prerequisite: PostgreSQL 17 and `psql` on PATH (see [`../../setup/POSTGRESQL_SETUP.md`](../../setup/POSTGRESQL_SETUP.md)).

Connection used by the project: host `localhost`, port `5432`, database `payflow`, user `course_user`, password `change_me`.
JDBC URL: `jdbc:postgresql://localhost:5432/payflow`

| Script | Purpose | Run as |
|--------|---------|--------|
| `00_create_database.sql` | Role `course_user` + database `payflow` (idempotent) | superuser |
| `01_schema.sql` | Tables, constraints, indexes | `course_user` |
| `02_seed_data.sql` | Demo users, accounts, a transfer and ledger entries | `course_user` |
| `03_procedures.sql` | `fn_monthly_statement(account, year, month)` PL/pgSQL function | `course_user` |
| `99_reset.sql` | Drops everything | `course_user` |

## macOS

```bash
brew services start postgresql@17
cd "Project 02 - PayFlow Wallet & Banking API"
psql -d postgres -f database/00_create_database.sql
psql -U course_user -h localhost -d payflow -f database/01_schema.sql
psql -U course_user -h localhost -d payflow -f database/02_seed_data.sql
psql -U course_user -h localhost -d payflow -f database/03_procedures.sql
psql -U course_user -h localhost -d payflow -c "SELECT * FROM fn_monthly_statement(1, EXTRACT(YEAR FROM now())::int, EXTRACT(MONTH FROM now())::int);"
```

## Windows (PowerShell)

```powershell
cd "Project 02 - PayFlow Wallet & Banking API"
psql -U postgres -h localhost -d postgres -f database\\00_create_database.sql
psql -U course_user -h localhost -d payflow -f database\\01_schema.sql
psql -U course_user -h localhost -d payflow -f database\\02_seed_data.sql
psql -U course_user -h localhost -d payflow -f database\\03_procedures.sql
psql -U course_user -h localhost -d payflow -c "SELECT * FROM fn_monthly_statement(1, 2025, 3);"
```

Quoting tip: always wrap the folder name in double quotes because it contains spaces and an `&`.

## Verify the seed data

```sql
SELECT a.account_number, a.balance, (SELECT balance_after FROM ledger_entries le WHERE le.account_id = a.id ORDER BY le.id DESC LIMIT 1) AS ledger_balance
FROM accounts a ORDER BY a.id;     -- balance must equal ledger_balance (account 4 has no entries)
```

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `password authentication failed` | `ALTER ROLE course_user PASSWORD 'change_me';` as superuser |
| `database "payflow" does not exist` | Run `00_create_database.sql` |
| `\\gexec` not understood | Use `psql`, not a GUI; or run `CREATE DATABASE payflow OWNER course_user;` manually |
| `Schema-validation: missing table` | Scripts were applied to a different database than `DB_URL` |
| Function returns no rows | The account has no ledger entries in that month (seed data is relative to *this* month and last month) |
"""

DATA_MODEL = """# PayFlow - Data Model

```mermaid
erDiagram
    USERS ||--o{ ACCOUNTS : owns
    USERS ||--o{ IDEMPOTENCY_KEYS : "sends keys"
    ACCOUNTS ||--o{ LEDGER_ENTRIES : "has entries"
    ACCOUNTS ||--o{ TRANSFERS : "is source (from)"
    ACCOUNTS ||--o{ TRANSFERS : "is target (to)"
    TRANSFERS ||--o{ LEDGER_ENTRIES : "produces 2 entries"
    TRANSFERS ||--o| IDEMPOTENCY_KEYS : "is recorded by"

    USERS { bigint id PK
            varchar email UK
            varchar password_hash
            varchar role "CUSTOMER | ADMIN" }
    ACCOUNTS { bigint id PK
               bigint owner_id FK
               varchar account_number UK
               char currency
               numeric balance "CHECK >= 0"
               varchar status "ACTIVE | FROZEN | CLOSED"
               bigint version "optimistic lock" }
    TRANSFERS { bigint id PK
                bigint from_account_id FK
                bigint to_account_id FK
                numeric amount "> 0"
                varchar status "PENDING | COMPLETED | FAILED" }
    LEDGER_ENTRIES { bigint id PK
                     bigint account_id FK
                     bigint transfer_id FK
                     varchar entry_type "DEPOSIT | WITHDRAWAL | DEBIT | CREDIT"
                     numeric amount
                     numeric balance_after
                     timestamptz created_at }
    IDEMPOTENCY_KEYS { bigint user_id PK
                       varchar idem_key PK
                       varchar request_hash
                       bigint transfer_id FK }
```

## Core invariants

1. `accounts.balance >= 0` (database CHECK) - no overdrafts.
2. Every balance change writes **exactly one** ledger entry whose `balance_after` equals the new balance.
3. A transfer writes **two** entries (DEBIT on the source, CREDIT on the target) in the **same transaction** as the two balance updates and the transfer row.
4. Ledger entries are append-only: no `UPDATE`/`DELETE` from the application.
5. Same user + same `Idempotency-Key` + same request body => the original result, no second money movement.
6. Same key + **different** body => `422 Unprocessable Entity`.
7. Transfers need `ACTIVE` accounts, equal currencies, `amount > 0` with at most 4 decimals.

## Transfer algorithm (service layer)

```mermaid
sequenceDiagram
    participant C as Client
    participant API as TransferService (@Transactional)
    participant DB as PostgreSQL
    C->>API: POST /api/transfers (Idempotency-Key: K)
    API->>DB: SELECT idempotency_keys WHERE (user, K)
    alt key exists, same hash
        API-->>C: 200 stored transfer (no new money movement)
    else key exists, other hash
        API-->>C: 422
    else new key
        API->>DB: load both accounts (ordered by id to avoid deadlocks)
        API->>API: validate status, currency, funds
        API->>DB: UPDATE accounts SET balance..., version = version + 1 (optimistic check)
        API->>DB: INSERT transfer, 2 ledger entries, idempotency key
        DB-->>API: commit
        API-->>C: 201 transfer
    end
```

### Concurrency strategy

- `@Version` on `Account`: two concurrent transfers from the same account cannot both read the old balance - one fails with `OptimisticLockingFailureException` -> retry (max 3) or answer 409.
- Always touch accounts in **ascending id order** (pessimistic or optimistic) to prevent deadlocks.
- The unique primary key `(user_id, idem_key)` makes duplicate concurrent submissions fail at the database; catch it and return the stored result.

## Monthly statement

`SELECT * FROM fn_monthly_statement(:accountId, :year, :month)` returns the entries of the month with `debit`, `credit` and `running_balance`
(see `database/03_procedures.sql`).
"""

README = """# Project 02 - PayFlow Wallet & Banking API

A wallet/banking backend: customers hold accounts, deposit and withdraw money and transfer between accounts safely. The focus is
**correctness under concurrency and retries**: transactions, optimistic locking (`@Version`), an append-only ledger and
idempotency keys.

| | |
|---|---|
| Stack | Java 21, Spring Boot 3.4.x (course target: Boot 4), Spring Data JPA, PostgreSQL 17, Maven |
| Package | `com.javaprep.payflow` |
| Port | `8080` |
| Database | `payflow` on `localhost:5432` (JDBC URL `jdbc:postgresql://localhost:5432/payflow`) |

Documents: [`PROJECT_INSTRUCTIONS.md`](PROJECT_INSTRUCTIONS.md) · [`DATA_MODEL.md`](DATA_MODEL.md) · [`GRADING_CRITERIA.md`](GRADING_CRITERIA.md) · [`database/DATABASE_SETUP.md`](database/DATABASE_SETUP.md)

## Prerequisites

JDK 21, Maven 3.9+, PostgreSQL 17 with `psql`; Days 25-27 (transactions), 35-40 (JPA/Security), 46 (idempotency/outbox), 47-48 (capstone).

## Quick start

```bash
cd "Project 02 - PayFlow Wallet & Banking API"

psql -d postgres -f database/00_create_database.sql
psql -U course_user -h localhost -d payflow -f database/01_schema.sql
psql -U course_user -h localhost -d payflow -f database/02_seed_data.sql
psql -U course_user -h localhost -d payflow -f database/03_procedures.sql

cp backend/src/main/resources/application-local.yml.example backend/src/main/resources/application-local.yml
cd backend
mvn spring-boot:run -Dspring-boot.run.profiles=local
curl http://localhost:8080/
mvn test        # H2, no PostgreSQL required
```

## CRITICAL: database connection (`application-local.yml`)

`backend/src/main/resources/application.yml` contains placeholders only:

```yaml
spring:
  datasource:
    url: ${DB_URL}
    username: ${DB_USERNAME}
    password: ${DB_PASSWORD}
```

### Option A (recommended): `application-local.yml`

1. Copy the template
   - macOS/Linux: `cp backend/src/main/resources/application-local.yml.example backend/src/main/resources/application-local.yml`
   - Windows: `Copy-Item backend\\src\\main\\resources\\application-local.yml.example backend\\src\\main\\resources\\application-local.yml`
2. Fill in your values:
   ```yaml
   spring:
     datasource:
       url: jdbc:postgresql://localhost:5432/payflow
       username: course_user
       password: change_me
   ```
3. Run with the `local` profile: `mvn spring-boot:run -Dspring-boot.run.profiles=local` (IntelliJ: *Active profiles* = `local`).
4. The file is **git-ignored** - confirm with `git status` and **never commit it**.

### Option B: environment variables

```bash
export DB_URL=jdbc:postgresql://localhost:5432/payflow DB_USERNAME=course_user DB_PASSWORD=change_me   # macOS/Linux
```
```powershell
$env:DB_URL="jdbc:postgresql://localhost:5432/payflow"; $env:DB_USERNAME="course_user"; $env:DB_PASSWORD="change_me"   # Windows
```

| Error | Meaning |
|-------|---------|
| `Could not resolve placeholder 'DB_URL'` | No `local` profile and no environment variables |
| `Connection refused` | PostgreSQL not running |
| `password authentication failed` | Wrong password |
| `Schema-validation: missing table` | SQL scripts not applied to this database |

## Seed accounts

Plain-text passwords below are for **local development only**; the SQL stores the BCrypt hashes (cost 10).

| Email | Role | Plain password | BCrypt hash stored in SQL |
|-------|------|----------------|---------------------------|
| `admin@payflow.com` | ADMIN | `Admin@123` | `@@ADMIN@@` |
| `alice@payflow.com` | CUSTOMER (accounts 1 and 3) | `Alice@123` | `@@ALICE@@` |
| `bob@payflow.com` | CUSTOMER (accounts 2 and 4 - frozen) | `Bob@123` | `@@BOB@@` |

Seed balances: account 1 = 1300.00, account 2 = 500.00, account 3 = 2000.00, account 4 = 0.00 (FROZEN), all USD.

## Layout

```
Project 02 - PayFlow Wallet & Banking API/
  README.md  PROJECT_INSTRUCTIONS.md  DATA_MODEL.md  GRADING_CRITERIA.md
  database/  00_create_database.sql  01_schema.sql  02_seed_data.sql  03_procedures.sql (fn_monthly_statement)  99_reset.sql  DATABASE_SETUP.md
  backend/   Spring Boot skeleton (see PROJECT_INSTRUCTIONS.md for the package plan)
```
"""

INSTR = """# PayFlow - Project Instructions

## 1. Goal

Implement a trustworthy money-movement API. Wrong answers here lose money, so correctness, auditability and safe retries matter
more than breadth.

## 2. Rules

- Java 21, Spring Boot skeleton in `backend/`, PostgreSQL, Maven. No Lombok, no Docker.
- Money is `BigDecimal` mapped to `NUMERIC(19,4)`; never `double`. Currency is a 3-letter ISO code; transfers need equal currencies.
- All state changes happen in `@Transactional` service methods; controllers contain no business logic.
- `Account` has `@Version`; the ledger is append-only.
- JWT or Basic authentication (instructor's choice), BCrypt passwords, `ProblemDetail` errors.
- Secrets via environment / `application-local.yml` only.

## 3. Milestones

### Milestone A - Foundations
Start against PostgreSQL, authentication (register/login), `Account` entity mapped with `ddl-auto=validate`, `GET /api/accounts` (own accounts).

### Milestone B - Deposits, withdrawals and the ledger
`POST /api/accounts/{id}/deposits`, `.../withdrawals`. Each writes balance change + ledger entry atomically. Overdraft -> 409 (`INSUFFICIENT_FUNDS`).
Tests: ledger `balance_after` always equals the account balance.

### Milestone C - Transfers with transactions
`POST /api/transfers {fromAccountId, toAccountId, amount, currency}` - debit, credit, transfer row and two ledger entries in one transaction.
Validations: owner of the source account, ACTIVE accounts, currency, positive amount (max 4 decimals), distinct accounts. Any failure leaves **no** partial change.

### Milestone D - Concurrency and idempotency
- `@Version` optimistic locking; retry on `OptimisticLockingFailureException` (max 3) or answer 409.
- Accounts are always locked/updated in ascending id order.
- `Idempotency-Key` header required on `POST /api/transfers`; behavior defined in `DATA_MODEL.md` (replay -> original result; different body -> 422).
- Tests: 20 parallel transfers from one account never overdraw; replaying a request moves money once.

### Milestone E - Statements and hardening
- Call `fn_monthly_statement` from Java: `GET /api/accounts/{id}/statements?year=&month=` (owner only; 404 for strangers).
- Finish the function's TODO (opening/closing rows). Validate month/year; paged transfer history `GET /api/transfers?accountId=&page=&size=`.
- Error contract, security matrix, test pyramid, production notes (profiles, secrets, JAR, CI).

## 4. API contract

| Method | Path | Role | Description | Success | Errors |
|--------|------|------|-------------|---------|--------|
| POST | `/api/auth/register` | public | `{email, password, fullName}` -> CUSTOMER | 201 | 400, 409 |
| POST | `/api/auth/login` | public | -> `{token}` | 200 | 401 |
| GET | `/api/accounts` | CUSTOMER | Own accounts | 200 | 401 |
| POST | `/api/accounts` | CUSTOMER | Open account `{currency}` | 201 | 400 |
| POST | `/api/accounts/{id}/deposits` | owner | `{amount, description}` | 201 `LedgerEntry` | 400, 404, 409 |
| POST | `/api/accounts/{id}/withdrawals` | owner | `{amount, description}` | 201 | 400, 404, 409 |
| POST | `/api/transfers` | owner of source | Header `Idempotency-Key`; body `{fromAccountId,toAccountId,amount,currency}` | 201 / 200 replay | 400, 404, 409, 422 |
| GET | `/api/transfers` | owner | Paged history | 200 | 404 |
| GET | `/api/accounts/{id}/statements` | owner | Monthly statement (calls `fn_monthly_statement`) | 200 | 400, 404 |
| PATCH | `/api/admin/accounts/{id}/status` | ADMIN | Freeze/unfreeze `{status}` | 200 | 403, 404 |

Error codes (in `ProblemDetail.properties.code`): `INSUFFICIENT_FUNDS`, `ACCOUNT_NOT_ACTIVE`, `CURRENCY_MISMATCH`, `IDEMPOTENCY_KEY_REUSED`, `CONCURRENT_MODIFICATION`.

## 5. User stories

1. As a customer I can open an account and see my balances.
2. As a customer I can deposit and withdraw, and my balance never goes negative.
3. As a customer I can transfer money to another account; either both sides change or neither.
4. As a customer I can safely retry a transfer after a timeout without paying twice.
5. As a customer I can download my monthly statement with a running balance.
6. As an admin I can freeze an account; frozen accounts reject all money movements.
7. As an auditor I can reconstruct every balance from the ledger.

## 6. Security requirements

- BCrypt, stateless tokens with expiry, secrets from env.
- Object-level checks: only the owner sees/uses an account (strangers get 404).
- Idempotency keys scoped per user (cannot collide across users).
- Never log tokens, passwords or full request bodies containing amounts+account numbers at INFO level.
- Rate-limit idea (document only): throttle `POST /api/transfers` per user.

## 7. Testing expectations

- Unit tests for the transfer decision logic (funds, status, currency).
- `@DataJpaTest` for ledger/balance consistency queries (H2) and optimistic locking.
- Concurrency test with an `ExecutorService` hitting the same account.
- PostgreSQL-only parts (`fn_monthly_statement`) are verified manually or with a test profile pointing at a real local database - document how.

## 8. Deliverables

Code, tests, README addendum with sample curl commands (including an idempotent retry), `DESIGN_NOTES.md` (locking strategy, failure modes).
"""

GRADING = """# PayFlow - Grading Criteria (100 points)

| Category | Points | What graders look for |
|----------|-------:|-----------------------|
| Foundations and auth (A) | 8 | Starts via `application-local.yml`/env, authentication, mapping validates |
| Deposits/withdrawals and ledger (B) | 14 | Atomic balance + ledger, no overdraft, `balance_after` consistency |
| Transfers (C) | 18 | One transaction, all validations, no partial changes on failure |
| Concurrency and idempotency (D) | 24 | `@Version`, retry/409 policy, ordered locking, key replay + 422 on reuse, parallel tests |
| Statements and SQL function (E) | 10 | Function called correctly, owner-only, opening/closing rows, input validation |
| Security | 8 | Object-level authorization, safe errors, no secrets committed |
| Testing | 10 | Concurrency + unit + slice tests, `mvn test` green without PostgreSQL |
| Code quality, docs, Git | 8 | Layering, BigDecimal usage, README, commit hygiene |

## Automatic deductions

- `double`/`float` used for money: **-10**
- Balance updated without a ledger entry (or vice versa): **-10**
- Idempotency implemented only in memory (not durable): **-5**
- Secrets or `application-local.yml` committed: **-10**
- `mvn test` red on a clean checkout: **-15**

## AI grading prompt

```
You are grading Project 02 (PayFlow Wallet & Banking API). Use only repository evidence, `mvn test` output and the README.
Check: BigDecimal everywhere, transfer atomicity (debit+credit+ledger in one transaction), @Version on Account, ordered account access,
Idempotency-Key semantics (replay returns the stored result, different body -> 422), ledger append-only, owner-only access (404),
no secrets committed. Score /100 using GRADING_CRITERIA.md weights and list blocking issues first.
```
"""


def build(root: Path) -> None:
    base = root / NAME
    kw = dict(ADMIN=HASH["admin"], ALICE=HASH["alice"], BOB=HASH["bob"])
    write(base / "README.md", sub(README, **kw))
    write(base / "PROJECT_INSTRUCTIONS.md", INSTR)
    write(base / "DATA_MODEL.md", DATA_MODEL)
    write(base / "GRADING_CRITERIA.md", GRADING)
    db = base / "database"
    write(db / "00_create_database.sql", CREATE_DB)
    write(db / "01_schema.sql", SCHEMA)
    write(db / "02_seed_data.sql", sub(SEED, **kw))
    write(db / "03_procedures.sql", PROC)
    write(db / "99_reset.sql", RESET)
    write(db / "DATABASE_SETUP.md", DB_SETUP)
    write_service(base / "backend", pkg="payflow", cls="PayFlow", artifact="payflow-backend", title="PayFlow Wallet and Banking API",
                  desc="PayFlow wallet and banking REST API (course project 02)", appname="payflow", db=DB, port=8080)
