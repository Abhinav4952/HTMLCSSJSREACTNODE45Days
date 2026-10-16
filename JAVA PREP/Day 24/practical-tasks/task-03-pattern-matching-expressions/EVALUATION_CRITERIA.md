# Evaluation Criteria — Day 24 — Task 03 — Pattern Matching over a Sealed Expression Tree

## Scope

Graded: the behavior and quality of the implementation in `PatternLab.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `eval(expr, env)` evaluates `Num`, `Var` (looked up in `env`; unbound -> `IllegalArgumentException("unbound variable: x")`), `Add`, `Mul`, and `Neg` with an **exhaustive switch without `default`**
- Requirement 2: `show(expr)` renders `Num` (negative numbers in parentheses: `(-3)`), `Var` (its name), `Add` as `(l + r)`, `Mul` as `(l * r)`, and `Neg` as `-` + operand; use a guard (`when`) for negative numbers
- Requirement 3: `simplify(expr)` simplifies **bottom-up**: constant folding for `Add`/`Mul` of two numbers, `0 + x = x`, `x + 0 = x`, `1 * x = x`, `x * 1 = x`, `0 * x = 0`, `x * 0 = 0`, `-(-x) = x`, `-(Num n) = Num(-n)`
- Requirement 4: `variables(expr)` returns the sorted set of variable names used in the tree
- Requirement 5: `describe(object)` returns: `null` -> `"null"`; negative `Integer` -> `"negative int <n>"`; other `Integer` -> `"int <n>"`; blank `String` -> `"blank string"`; other `String` -> `"string of length <n>"`; `int[]` -> `"int array of <n>"`; empty `List` -> `"empty list"`; other `List` -> `"list of <n>"`; `Expr` -> `"expression "` + `show(expr)`; anything else -> `"other: <SimpleName>"`

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- unbound variables
- nested negation
- simplification that cascades (a rule enabling another)
- guard order (specific before general)

### Day-specific checks

- No `default` in the switches over `Expr` (exhaustiveness checking is intentional)
- No `instanceof` + cast chains where a pattern fits
- Guards and case order are deliberate

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`, JaCoCo summary (`target/site/jacoco/index.html`)

## AI-assisted grading prompt (optional)

```
You are grading Day 24 Task 03 (Pattern Matching over a Sealed Expression Tree) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `PatternLab.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
