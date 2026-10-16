# Evaluation Criteria — Day 25 — Task 01 — Create Tables and Constraints

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 25 Task 01 (`create-tables-constraints`).

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

- Create `customers`, `products`, `orders` in `sql/schema.sql` with the exact column names from the TODO comments.
- Use identity primary keys, a UNIQUE email and sku, NOT NULL where specified, a CHECK on price and order status, and defaults for `created_at`, `status`, `placed_at`.
- Add the foreign key `orders.customer_id -> customers.id`.
- Fill the two blocks in `sql/answers.sql` (keep the `-- @name` markers).

### Edge cases

- Constraint violations must raise `SQLException` (never silently coerce).
- Status default must be exactly `NEW`.
- Seed data must load cleanly after your schema (no extra columns required).

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day25-task01)`

## AI grading prompt (paste into your grader)

```
You are grading Day 25 Task 01 (Create Tables and Constraints) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
