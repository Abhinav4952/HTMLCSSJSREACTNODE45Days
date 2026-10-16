# Evaluation Criteria — Day 28 — Task 04 — Java Config and @Value

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 28 Task 04 (`config-bean-lab`).

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

- Add `@Value("${tax.rate:0.2}")` to the `taxPolicy` parameter and validate the range.
- Implement both `@Bean` methods.
- Show the default and an overridden property both work.

### Edge cases

- Rate must be within 0..1 inclusive; otherwise context startup fails.
- Both beans are singletons: the calculator must receive the container's `TaxPolicy`.

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day28-task04)`

## AI grading prompt (paste into your grader)

```
You are grading Day 28 Task 04 (Java Config and @Value) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
