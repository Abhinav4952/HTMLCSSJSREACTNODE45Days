# Evaluation Criteria — Day 40 — Task 04 — Aspect Ordering with @Order

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 40 Task 04 (`aspect-ordering-challenge`).

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

- Make both classes aspect beans with explicit precedence (`@Order(1)` outer, `@Order(2)` inner).
- Reference the shared pointcut `Pointcuts.payment()` from both advices.
- Implement both around bodies so the recorded sequence is onion-shaped.

### Edge cases

- Lower `@Order` value = higher precedence = outermost.
- An exception must travel through `tx:rollback` first, then `security:out`.
- Without `@Order` the order is undefined.

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day40-task04)`

## AI grading prompt (paste into your grader)

```
You are grading Day 40 Task 04 (Aspect Ordering with @Order) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
