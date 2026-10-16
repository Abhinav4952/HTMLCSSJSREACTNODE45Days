# PayFlow - Grading Criteria (100 points)

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
