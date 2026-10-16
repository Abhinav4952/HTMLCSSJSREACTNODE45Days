# PayFlow - Project Instructions

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
