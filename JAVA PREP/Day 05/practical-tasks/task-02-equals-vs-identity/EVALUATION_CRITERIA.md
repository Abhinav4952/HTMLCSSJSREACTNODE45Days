# Evaluation Criteria — Day 05 — Task 02 — Equals vs Identity

## Scope

Automated JUnit verification plus light code-quality review for Day 05 Task 02.

## Weighting (100 points)

| Category | Points |
|----------|-------:|
| Correctness (tests + edge cases) | 70 |
| API / exception contracts | 15 |
| Code clarity (naming, simplicity) | 10 |
| Git / hygiene (no target/, no secrets) | 5 |

## Pass / fail gates (automatic fail if violated)

- Code does not compile
- `mvn test` fails
- Secrets or `target/` committed
- Lombok or forbidden APIs used when constraints forbid them

## Detailed rubric

### Correctness

- All required behaviors implemented
- Edge cases match TODOs

### Edge cases

- Null / illegal inputs handled as specified

### Security / privacy (if applicable)

- N/A unless task involves secrets or SQL

### UX / accessibility (if applicable)

- N/A (backend / library task)

## Evidence the grader should collect

- `mvn test` console output
- Diff of `StringCompare.java`

## AI grading prompt (paste into your grader)

```
You are grading Day 05 Task 02 (Equals vs Identity) for a graduate Java backend course.
Use only observable evidence. Run or trust mvn test results.
Score /100 using the rubric weights. List blocking issues first.
Leftover TODO comments are OK if behavior is implemented and tests pass.
```
