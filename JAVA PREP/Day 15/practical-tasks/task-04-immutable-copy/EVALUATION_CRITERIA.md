# Evaluation Criteria — Day 15 — Task 04 — Immutable Roster with Defensive Copies

## Scope

Graded: the behavior and quality of the implementation in `Roster.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `new Roster(names, scores)` stores immutable copies (`List.copyOf`, `Map.copyOf`); null arguments or null elements throw `NullPointerException`
- Requirement 2: Changes to the caller's original collections after construction do not affect the roster
- Requirement 3: `names()` and `scores()` return collections that throw `UnsupportedOperationException` on mutation
- Requirement 4: `withName(String)` returns a **new** roster that has one more name (appended) and the same scores; the original is unchanged
- Requirement 5: `safeCopy(Collection<? extends T>)` returns an immutable `List<T>` snapshot
- Requirement 6: `viewReflectsChanges(base)` returns `true` (an unmodifiable view shows later changes to its base) and `copyIgnoresChanges(base)` returns `true` (an immutable copy does not); both must actually perform the experiment on a **copy** of `base` and not mutate `base`

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- null list, null element, null map
- mutating the original after construction
- wither leaves original untouched
- `Map.copyOf` iteration order is unspecified - do not depend on it

### Day-specific checks

- No field is ever exposed in mutable form
- `unmodifiableList` over internal state is avoided and justified in a comment
- Constructor performs the defensive copy (copy-in), getters return immutables (copy-out not needed)

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 15 Task 04 (Immutable Roster with Defensive Copies) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `Roster.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
