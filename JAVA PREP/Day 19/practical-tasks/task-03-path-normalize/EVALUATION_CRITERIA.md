# Evaluation Criteria — Day 19 — Task 03 — Path Normalize and Traversal Guard

## Scope

Graded: the behavior and quality of the implementation in `PathTools.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `normalized(String)` returns `Path.of(text).normalize()`
- Requirement 2: `segments(Path)` returns the name elements as strings (root excluded); an empty path gives an empty list
- Requirement 3: `extension(Path)` returns the text after the last dot of the file name, or `""` when none (hidden files like `.bashrc` and names ending with `.` have no extension)
- Requirement 4: `changeExtension(file, newExt)` replaces (or adds) the extension, keeping the parent directory
- Requirement 5: `relativeTo(base, target)` returns the relative path from `base` to `target`
- Requirement 6: `resolveSafe(base, userPath)` returns the normalized absolute path under `base`; throws `IllegalArgumentException` if the result escapes `base` (including absolute `userPath`s and `../` tricks)

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- `..` that stays inside the base (allowed)
- `..` that leaves the base (rejected)
- absolute user path
- hidden files and trailing dots

### Day-specific checks

- `Path` API used instead of string concatenation
- `resolveSafe` normalizes before the `startsWith` check
- No file system access in this class

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 19 Task 03 (Path Normalize and Traversal Guard) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `PathTools.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
