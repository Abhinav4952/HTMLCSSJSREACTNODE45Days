# Evaluation Criteria — Day 22 — Task 03 — Class Loader Lab

## Scope

Graded: the behavior and quality of the implementation in `ClassLoaderLab.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `bytesOf(type)` reads the `.class` bytes of a loaded class from its resource (`/pkg/Name.class`); a missing resource -> `IllegalArgumentException`
- Requirement 2: `IsolatedLoader(parent, classes)` defines each registered class name **itself** (child-first, once per loader, synchronized on the class-loading lock) and delegates every other name to the parent
- Requirement 3: `loaderName(type)` returns `bootstrap` when the class loader is `null`, the loader's name when it has one (`app`, `platform`), otherwise the loader's simple class name
- Requirement 4: `loaderChain(loader)` lists loader names from the given loader up to and including `bootstrap`
- Requirement 5: `instantiate(type)` creates an instance via the public no-arg constructor, wrapping reflective failures in `IllegalStateException` with the cause

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- unknown class names throw `ClassNotFoundException`
- java.* classes must still come from the parent
- loading the same name twice in one loader returns the same `Class`
- classes without a registered name delegate to the parent (same `Class` as the app loader)

### Day-specific checks

- Delegation preserved for everything that is not registered
- Class identity reasoning is correct (name + loader)
- Locking on `getClassLoadingLock(name)`

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 22 Task 03 (Class Loader Lab) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `ClassLoaderLab.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
