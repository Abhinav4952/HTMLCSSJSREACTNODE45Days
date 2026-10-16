# Task 4 — Employee Comparator Chain

**Day:** 14 · **Task ID:** Day14-task04 · **Type:** Plain Java · **Difficulty:** Challenge

## Summary

Compose multi-key comparators with `Comparator.comparing(...).thenComparing(...)`, build a null-safe case-insensitive string comparator, fold a list of comparators into one, and produce a sorted **copy** without touching the original list. Challenge: do it without writing any hand-rolled `compare` bodies using subtraction.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day14/task04/Employee.java` | Provided type (no changes needed) |
| `src/main/java/com/javaprep/day14/task04/EmployeeSorts.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day14/task04/EmployeeSortsTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 14 theory file read

## What you will implement

1. `byDeptThenSalaryDescThenName()` orders by department ascending, then salary **descending**, then name ascending
2. `byNameIgnoreCaseNullsLast()` compares strings case-insensitively, with `null` sorted last
3. `chain(List<Comparator<T>>)` returns a comparator applying the given comparators in order; an empty list treats all elements as equal
4. `sortedCopy(list, comparator)` returns a new sorted list (stable) and leaves the input unchanged

## Constraints

- Do not write comparator lambdas that subtract numbers
- Do not edit the tests
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=EmployeeSortsTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **7 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day14-task04)`).

### Run one test class

```bash
mvn -Dtest=EmployeeSortsTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `EmployeeSorts.java` — `byDeptThenSalaryDescThenName` | `TODO(Day14-task04)` | dept ascending, then salary descending, then name ascending, built with Comparator.comparing/thenComparing (no subtraction) |
| `EmployeeSorts.java` — `byNameIgnoreCaseNullsLast` | `TODO(Day14-task04)` | case-insensitive String comparator that sorts null last |
| `EmployeeSorts.java` — `chain` | `TODO(Day14-task04)` | combine comparators so that later ones only break ties of earlier ones; empty list -> everything equal |
| `EmployeeSorts.java` — `sortedCopy` | `TODO(Day14-task04)` | return a new ArrayList sorted with comparator (stable); do not modify input |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_deptThenSalaryDescThenName`, `r1_comparatorIsSymmetric` |
| 2 | `r2_nameIgnoreCaseNullsLast` |
| 3 | `r3_chainAppliesComparatorsInOrder`, `r3_emptyChainTreatsEverythingEqual` |
| 4 | `r4_sortedCopyLeavesInputUntouched`, `r4_sortIsStable` |

## Edge cases to handle

- equal salaries fall through to name
- nulls in the string comparator
- empty comparator list
- stability for elements the comparator considers equal

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 14: Employee Comparator Chain`

## Hints (optional)

<details><summary>Hint 1</summary>

`Comparator.comparing(f).thenComparing(g, Comparator.reverseOrder())` handles descending keys.

</details>

<details><summary>Hint 2</summary>

`chain` can start from `(a, b) -> 0` and apply `thenComparing` repeatedly.

</details>
