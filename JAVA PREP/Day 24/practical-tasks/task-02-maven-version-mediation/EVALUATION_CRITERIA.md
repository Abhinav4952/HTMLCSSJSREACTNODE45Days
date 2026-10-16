# Evaluation Criteria — Day 24 — Task 02 — Maven Versions, Ranges, and Dependency Mediation

## Scope

Graded: the behavior and quality of the implementation in `MavenVersion.java`, `VersionRange.java`, `DependencyMediation.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `MavenVersion.parse(text)` accepts `N(.N)*` optionally followed by `-qualifier` where the qualifier is `alpha|beta|milestone|rc|cr|snapshot|ga|final` (case-insensitive) with an optional number (`rc1`, `rc.2`, `beta-3`); otherwise `IllegalArgumentException` (also for null/blank)
- Requirement 2: `MavenVersion` implements `Comparable`: numeric components compare numerically with missing components treated as 0 (`1.0 == 1.0.0`), then qualifiers by rank `alpha < beta < milestone < rc(=cr) < snapshot < release(none/ga/final)`, then the qualifier number; `equals`/`hashCode` are consistent with `compareTo`
- Requirement 3: `VersionRange.parse(spec)` supports `[a,b]`, `[a,b)`, `(a,b]`, `(a,b)`, `[a,)`, `(,b]` and the exact form `[a]`; anything else (plain `1.0`, empty bounds on both sides, lower > upper) -> `IllegalArgumentException`; `contains(version)` honours inclusive/exclusive bounds
- Requirement 4: `DependencyMediation.resolve(declarations)` picks, for every `groupId:artifactId`, the declaration with the **smallest depth** (ties: first declared) and returns `artifact -> version` in order of first appearance
- Requirement 5: `DependencyMediation.highest(versions)` returns the highest version string (by `MavenVersion` ordering; empty -> `IllegalArgumentException`) and `satisfying(range, versions)` returns the matching version strings sorted ascending

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- `1.10` vs `1.9`
- `1.0` vs `1.0.0`
- SNAPSHOT vs release vs rc
- unbounded ranges

### Day-specific checks

- `compareTo` is consistent with `equals` and `hashCode`
- Range bounds handle unbounded sides without special-casing callers
- Mediation is deterministic (stable ties)

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`, JaCoCo summary (`target/site/jacoco/index.html`)

## AI-assisted grading prompt (optional)

```
You are grading Day 24 Task 02 (Maven Versions, Ranges, and Dependency Mediation) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `MavenVersion.java`, `VersionRange.java`, `DependencyMediation.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
