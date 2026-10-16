# PeopleHub - Grading Criteria (100 points)

| Category | Points | What graders look for |
|----------|-------:|-----------------------|
| Boundaries and database-per-service (A) | 10 | Each service starts with its own DB; no cross-DB FKs or shared tables; clean module structure |
| employee-service (B) | 12 | Auth, entities, paging, authorization |
| leave-service (C) | 18 | Business rules, balance logic, RestClient with timeout/retry/circuit breaker and fallback |
| Approval + outbox + Kafka producer (D) | 20 | One transaction for approval + outbox, poller semantics, JSON contract, EmbeddedKafka tests |
| notification-service consumer (E) | 14 | Consumer group, DLT/error handling, idempotency, owner-only endpoints |
| Gateway and security | 8 | Routes, JWT at the edge, request id, object-level checks, no secrets in Git |
| Testing | 10 | Unit/slice/Kafka tests, `mvn test` green without PostgreSQL/Kafka |
| Documentation and Git | 8 | README accuracy, per-service run notes, PR hygiene |

## Automatic deductions

- Cross-database foreign key or direct SQL access to another service's database: **-10**
- Kafka publish inside the approval transaction without outbox (dual write): **-8**
- Consumer without idempotency: **-8**
- `application-local.yml`, credentials or `target/` committed: **-10**
- `mvn test` red on a clean checkout: **-15**

## AI grading prompt

```
You are grading Project 03 (PeopleHub HR Microservices). Use repository evidence and `mvn test` output only.
Check: database per service, approval + outbox in one transaction, event contract matches docs/LEAVE_APPROVED_EVENT.md,
consumer idempotency + DLT, RestClient resilience with fallback, gateway routes + auth at the edge, owner-only access, no secrets committed.
Score /100 with GRADING_CRITERIA.md weights; list blocking issues first.
```
