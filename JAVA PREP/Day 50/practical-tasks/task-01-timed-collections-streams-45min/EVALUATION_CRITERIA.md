# Evaluation Criteria — Day 50 — Task 01 — Timed Round 1 (45 min): Collections and Streams

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 50 Task 01 (`timed-collections-streams-45min`).

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

- `topWords`: frequency count, deterministic ordering.
- `groupAnagrams`: stable grouping.
- `firstNonRepeated`: single pass counting with insertion order.
- `isBalanced`: stack-based matching.

### Edge cases

- Empty/null input.
- Ties in frequency.
- Case sensitivity differences between methods.
- Unbalanced closers at the start.

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day50-task01)`

## AI grading prompt (paste into your grader)

```
You are grading Day 50 Task 01 (Timed Round 1 (45 min): Collections and Streams) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
