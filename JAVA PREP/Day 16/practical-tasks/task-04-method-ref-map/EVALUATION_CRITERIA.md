# Evaluation Criteria — Day 16 — Task 04 — Method References Zoo

## Scope

Graded: the behavior and quality of the implementation in `MethodRefMap.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `parser()` returns a `Function<String,Integer>` using `Integer::parseInt` (static reference)
- Requirement 2: `upper()` returns a `Function<String,String>` using `String::toUpperCase` (unbound instance reference)
- Requirement 3: `prefixer(prefix)` returns a function that prepends `prefix`, using a bound reference (`prefix::concat`); `null` prefix throws `NullPointerException` immediately (when creating the reference)
- Requirement 4: `listFactory()` returns a `Supplier<List<String>>` producing a **new** empty mutable list each call (`ArrayList::new`)
- Requirement 5: `personFactory()` returns a `Function<String, Person>` using the `Person::new` constructor reference
- Requirement 6: `indexBy(values, keyFn)` returns a `LinkedHashMap` of key -> value in input order and throws `IllegalArgumentException` on duplicate keys

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- null prefix
- each listFactory call yields a distinct list
- duplicate keys
- empty input

### Day-specific checks

- Each of the four reference kinds is used where the task names it
- No lambda where a method reference works
- Fail-fast semantics of bound references understood and commented

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 16 Task 04 (Method References Zoo) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `MethodRefMap.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
