# Evaluation Criteria — Day 21 — Task 03 — CompletableFuture Pipeline

## Scope

Graded: the behavior and quality of the implementation in `CompletablePipeline.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `pipeline(source, executor)` runs `source` asynchronously on `executor`, trims the text, then upper-cases it
- Requirement 2: `combine(a, b)` completes with the sum of both results (`thenCombine`)
- Requirement 3: `allInOrder(futures)` completes with the list of all results in the **input order** (`allOf` + `join`)
- Requirement 4: `withFallback(risky, executor, fallback)` runs `risky` asynchronously and completes with `fallback` if it throws
- Requirement 5: `chain(id, lookupUser, lookupEmail)` runs `lookupUser(id)` then `lookupEmail(user)` using `thenCompose`
- Requirement 6: `withTimeout(future, millis, defaultValue)` completes with `defaultValue` when the future is not done in time (`completeOnTimeout`)
- Requirement 7: `describe(future)` returns `"ok:<value>"` or `"error:<root exception simple name>"`, unwrapping a `CompletionException`

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- failure in the middle of a chain
- future that never completes
- empty list in `allInOrder`
- wrapped vs direct exceptions in `describe`

### Day-specific checks

- No blocking `join()`/`get()` before the pipeline is composed (except inside already-completed stages)
- Correct operator choice: `thenCompose` vs `thenApply`
- Error handling unwraps `CompletionException`

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 21 Task 03 (CompletableFuture Pipeline) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `CompletablePipeline.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
