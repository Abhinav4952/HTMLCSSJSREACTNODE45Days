# Task 3 — TDD: Reverse Polish Notation Calculator

**Day:** 23 · **Task ID:** Day23-task03 · **Type:** Plain Java · **Difficulty:** Stretch

## Summary

Implement a bounded `Stack` and a Reverse Polish Notation (postfix) calculator **the TDD way**: the nested test classes describe the behaviour in the order you would have written them (stack basics -> arithmetic -> error handling). Run the tests, implement just enough for each group, and refactor.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day23/task03/BoundedStack.java` | Stubs with TODOs |
| `src/main/java/com/javaprep/day23/task03/RpnCalculator.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day23/task03/RpnCalculatorTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 23 theory file read

## What you will implement

1. `BoundedStack<T>(capacity)`: `push`, `pop`, `peek`, `size`, `isEmpty`, `capacity`; capacity must be > 0 (`IllegalArgumentException`); `push` on a full stack -> `IllegalStateException("stack full")`; `pop`/`peek` on an empty stack -> `NoSuchElementException`
2. `RpnCalculator(maxDepth)` evaluates whitespace-separated postfix expressions over `long` values with `+ - * /` (integer division truncating toward zero); `evaluate("3 4 + 2 *")` = 14
3. Errors: null/blank -> `IllegalArgumentException("empty expression")`; unknown token -> `IllegalArgumentException("unknown token: x")`; missing operands -> `IllegalArgumentException("not enough operands")`; leftover values -> `IllegalArgumentException("too many operands")`; `/` by zero -> `ArithmeticException("division by zero")`; exceeding `maxDepth` -> `IllegalStateException`
4. Arithmetic overflow is detected with `Math.addExact/subtractExact/multiplyExact` (`ArithmeticException`)

## Constraints

- Use your `BoundedStack` inside the calculator
- Do not edit the tests
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=RpnCalculatorTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **11 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day23-task03)`).

### Run one test class

```bash
mvn -Dtest=RpnCalculatorTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `BoundedStack.java` — `constructor` | `TODO(Day23-task03)` | capacity <= 0 -> IllegalArgumentException; allocate the backing array |
| `BoundedStack.java` — `push` | `TODO(Day23-task03)` | when size == capacity throw IllegalStateException("stack full"); otherwise store at items[size++] |
| `BoundedStack.java` — `pop` | `TODO(Day23-task03)` | empty -> NoSuchElementException; otherwise return the top element and clear its slot (avoid keeping a reference) |
| `BoundedStack.java` — `peek` | `TODO(Day23-task03)` | empty -> NoSuchElementException; otherwise return the top element without removing it |
| `RpnCalculator.java` — `evaluate` | `TODO(Day23-task03)` | null/blank -> IAE("empty expression"); split on whitespace; numbers (parse long) are pushed on a BoundedStack(maxDepth); + - * / pop right then left, apply (multiplyExact; "/" by zero -> ArithmeticException("division by zero")), push; too few operands -> IAE("not enough operands"); unknown token -> IAE("unknown token: x"); at the end exactly one value must remain else IAE("too many operands") |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_startsEmpty`, `r1_isLastInFirstOut`, `r1_rejectsPushWhenFull`, `r1_popAndPeekOnEmptyFail`, `r1_slotsAreReusableAfterPop`, `r1_capacityMustBePositive` |
| 2 | `r2_isReusableBetweenEvaluations`, `r2_detectsOverflow` |
| 3 | `r3_blankExpression`, `r3_nullExpression`, `r3_reportsTheProblem` |

## Edge cases to handle

- single number expression
- negative numbers (`-3` is a number, `-` is an operator)
- very long expressions vs `maxDepth`
- extra whitespace

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 23: TDD: Reverse Polish Notation Calculator`

## Hints (optional)

<details><summary>Hint 1</summary>

Start with the stack tests (small, no dependencies), then the happy-path arithmetic, then errors - exactly the order of the nested classes.

</details>

<details><summary>Hint 2</summary>

Treat any token that is not an operator as a number first; a `NumberFormatException` becomes `unknown token`.

</details>

<details><summary>Hint 3</summary>

Pop the **right** operand first - it matters for `-` and `/`.

</details>
