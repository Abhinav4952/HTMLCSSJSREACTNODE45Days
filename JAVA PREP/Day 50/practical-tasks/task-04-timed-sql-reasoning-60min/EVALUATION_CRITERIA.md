# Evaluation Criteria — Day 50 — Task 04 — Timed Round 4 (60 min): SQL Reporting and Index Reasoning

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 50 Task 04 (`timed-sql-reasoning-60min`).

## Weighting (100 points)

| Category | Points |
|----------|-------:|
| Correctness (all tests green, requirements met) | 60 |
| Edge cases and error contracts | 20 |
| Code clarity (naming, simplicity, idiomatic Spring/SQL) | 15 |
| Git / hygiene (no `target/`, no secrets, only intended files changed) | 5 |

## Pass / fail gates (automatic fail if violated)

- Project does not compile or `mvn test` fails
- Tests, `pom.xml`, or provided helpers modified to force a pass
- Hard-coded answers that special-case test inputs
- Secrets or `target/` committed

## Detailed rubric

### Correctness

- `topCustomersSql`: PAID totals per customer, top 2, name + total.
- `customersWithoutPaidOrdersSql`: anti-join with `NOT EXISTS`, ordered by name.
- `supportingIndexDdl`: composite index `(customer_id, status)` named `idx_orders_customer_status`.
- Be ready to explain: why `NOT EXISTS` over `NOT IN` (NULL semantics), and why the column order of the index matters.

### Edge cases

- Customers with no orders.
- Cancelled orders must not count.
- NULL handling in `NOT IN`.

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day50-task04)`

## AI grading prompt (paste into your grader)

```
You are grading Day 50 Task 04 (Timed Round 4 (60 min): SQL Reporting and Index Reasoning) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
