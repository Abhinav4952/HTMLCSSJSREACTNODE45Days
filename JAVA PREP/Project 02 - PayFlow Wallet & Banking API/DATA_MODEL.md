# PayFlow - Data Model

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
