# Evaluation Criteria — Day 23 — Task 03 — TDD: Reverse Polish Notation Calculator

## Scope

Graded: the behavior and quality of the implementation in `BoundedStack.java`, `RpnCalculator.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `BoundedStack<T>(capacity)`: `push`, `pop`, `peek`, `size`, `isEmpty`, `capacity`; capacity must be > 0 (`IllegalArgumentException`); `push` on a full stack -> `IllegalStateException("stack full")`; `pop`/`peek` on an empty stack -> `NoSuchElementException`
- Requirement 2: `RpnCalculator(maxDepth)` evaluates whitespace-separated postfix expressions over `long` values with `+ - * /` (integer division truncating toward zero); `evaluate("3 4 + 2 *")` = 14
- Requirement 3: Errors: null/blank -> `IllegalArgumentException("empty expression")`; unknown token -> `IllegalArgumentException("unknown token: x")`; missing operands -> `IllegalArgumentException("not enough operands")`; leftover values -> `IllegalArgumentException("too many operands")`; `/` by zero -> `ArithmeticException("division by zero")`; exceeding `maxDepth` -> `IllegalStateException`
- Requirement 4: Arithmetic overflow is detected with `Math.addExact/subtractExact/multiplyExact` (`ArithmeticException`)

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- single number expression
- negative numbers (`-3` is a number, `-` is an operator)
- very long expressions vs `maxDepth`
- extra whitespace

### Day-specific checks

- Messages match the tests; exception types are intentional
- Stack slots cleared on pop (no lingering references)
- No duplicated operator logic

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`, JaCoCo summary (`target/site/jacoco/index.html`)

## AI-assisted grading prompt (optional)

```
You are grading Day 23 Task 03 (TDD: Reverse Polish Notation Calculator) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `BoundedStack.java`, `RpnCalculator.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
