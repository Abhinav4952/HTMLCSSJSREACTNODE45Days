# Evaluation Criteria — Day 16 — Task 01 — Lambda Filter, Map, and Closures

## Scope

Graded: the behavior and quality of the implementation in `LambdaFilter.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

## Weighting (100 points unless the instructor overrides)

| Category | Points | Description |
|----------|-------:|-------------|
| Automated tests (`mvn test`) | 40 | Fraction of tests passing; no skipped/@Disabled tests |
| Requirements coverage | 25 | Each "What you will implement" bullet satisfied |
| Code quality | 20 | Naming, structure, idiomatic Java 21, no duplication, correct use of the day's concepts |
| Robustness & safety | 10 | Edge cases, null/validation handling, exceptions, thread-safety/security where relevant |
| Readability & process | 5 | Clear commits, formatting, sensible comments |

## Pass / fail gates (automatic fail if violated)

- Tests modified/disabled to force a pass
- Hard-coded secrets
- Forbidden APIs from Constraints used
- Project does not compile

## Detailed rubric

### Automated tests

- Full marks only when every test passes with no `@Disabled` and no edits to test files.
- Partial credit is proportional to passing tests; a compile failure scores 0 in this category.

### Requirements coverage

- Requirement 1: `filter(list, predicate)` returns a new list of elements matching the predicate (accepts `Predicate<? super T>`)
- Requirement 2: `mapAll(list, fn)` returns a new list of transformed elements (accepts `Function<? super T, ? extends R>`)
- Requirement 3: `applyTwice(f, x)` applies an `IntUnaryOperator` two times
- Requirement 4: `counter()` returns a `Supplier<Integer>`; each supplier yields 1, 2, 3, ... independently of other suppliers
- Requirement 5: `adders(n)` returns `n` `IntUnaryOperator`s where the operator at index `i` adds `i` to its argument

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- empty list
- predicate matching nothing/everything
- `adders(0)` is empty; negative `n` throws `IllegalArgumentException`
- two counters do not share state

### Day-specific checks

- No mutation of input lists
- Lambdas/method references used where natural
- Loop-variable capture handled with a per-iteration copy

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 16 Task 01 (Lambda Filter, Map, and Closures) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `LambdaFilter.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
