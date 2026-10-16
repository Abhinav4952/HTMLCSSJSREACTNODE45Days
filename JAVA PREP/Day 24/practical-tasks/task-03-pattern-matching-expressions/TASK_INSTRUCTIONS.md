# Task 3 — Pattern Matching over a Sealed Expression Tree

**Day:** 24 · **Task ID:** Day24-task03 · **Type:** Plain Java · **Difficulty:** Stretch

## Summary

Use Java 21 pattern matching end to end: evaluate, print, simplify, and analyse an expression tree built from sealed records with **record deconstruction patterns**, guards, and exhaustive switches; plus a `describe(Object)` method using type patterns, `case null`, array patterns, and `when` guards.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day24/task03/Expr.java` | Provided type (no changes needed) |
| `src/main/java/com/javaprep/day24/task03/PatternLab.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day24/task03/PatternLabTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 24 theory file read

## What you will implement

1. `eval(expr, env)` evaluates `Num`, `Var` (looked up in `env`; unbound -> `IllegalArgumentException("unbound variable: x")`), `Add`, `Mul`, and `Neg` with an **exhaustive switch without `default`**
2. `show(expr)` renders `Num` (negative numbers in parentheses: `(-3)`), `Var` (its name), `Add` as `(l + r)`, `Mul` as `(l * r)`, and `Neg` as `-` + operand; use a guard (`when`) for negative numbers
3. `simplify(expr)` simplifies **bottom-up**: constant folding for `Add`/`Mul` of two numbers, `0 + x = x`, `x + 0 = x`, `1 * x = x`, `x * 1 = x`, `0 * x = 0`, `x * 0 = 0`, `-(-x) = x`, `-(Num n) = Num(-n)`
4. `variables(expr)` returns the sorted set of variable names used in the tree
5. `describe(object)` returns: `null` -> `"null"`; negative `Integer` -> `"negative int <n>"`; other `Integer` -> `"int <n>"`; blank `String` -> `"blank string"`; other `String` -> `"string of length <n>"`; `int[]` -> `"int array of <n>"`; empty `List` -> `"empty list"`; other `List` -> `"list of <n>"`; `Expr` -> `"expression "` + `show(expr)`; anything else -> `"other: <SimpleName>"`

## Constraints

- Do not edit `Expr` or the tests
- No visitor pattern, no `instanceof` + explicit casts
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=PatternLabTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **16 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day24-task03)`).

### Run one test class

```bash
mvn -Dtest=PatternLabTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `PatternLab.java` — `eval` | `TODO(Day24-task03)` | exhaustive switch (no default) with record patterns: Num -> value; Var -> env lookup or IllegalArgumentException("unbound variable: <name>"); Add -> sum; Mul -> product; Neg -> negation |
| `PatternLab.java` — `show` | `TODO(Day24-task03)` | Num with a guard (negative -> "(-3)"), Num -> digits, Var -> name, Add -> "(l + r)", Mul -> "(l * r)", Neg -> "-" + show(inner) |
| `PatternLab.java` — `simplify` | `TODO(Day24-task03)` | bottom-up: simplify the children first, then apply: Add/Mul of two Num folds; 0+x=x, x+0=x, 1*x=x, x*1=x, 0*x=0, x*0=0; Neg(Num n)=Num(-n); Neg(Neg x)=x; otherwise rebuild the node |
| `PatternLab.java` — `variables` | `TODO(Day24-task03)` | collect Var names recursively into a TreeSet (sorted) |
| `PatternLab.java` — `describe` | `TODO(Day24-task03)` | switch with patterns in this order: null, negative Integer (guard), Integer, blank String (guard), String, int[], empty List (guard), List, Expr (use show), default "other: " + simple class name |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_evaluatesNestedExpressions`, `r1_usesTheEnvironmentForEveryVariable`, `r1_unboundVariableIsReported` |
| 2 | `r2_rendersInfixWithParentheses`, `r2_negativeNumbersAndNegation` |
| 3 | `r3_constantFolding`, `r3_identities`, `r3_negation`, `r3_rulesCascadeBottomUp`, `r3_unsimplifiableTreesAreRebuiltEqual`, `r3_simplifyPreservesTheValue` |
| 4 | `r4_collectsSortedVariableNames` |
| 5 | `r5_describesNullAndNumbers`, `r5_blankStrings`, `r5_stringsArraysAndLists`, `r5_expressionsAndOtherTypes` |

## Edge cases to handle

- unbound variables
- nested negation
- simplification that cascades (a rule enabling another)
- guard order (specific before general)
- null input to `describe`

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 24: Pattern Matching over a Sealed Expression Tree`

## Hints (optional)

<details><summary>Hint 1</summary>

Order matters in a pattern switch: put guarded cases (`when`) **before** the unguarded case of the same type.

</details>

<details><summary>Hint 2</summary>

In `simplify`, always simplify children **first**, then look at the simplified children - that is what makes the rules cascade.

</details>

<details><summary>Hint 3</summary>

A sealed hierarchy lets the switch be exhaustive without `default`; try adding a new record to `Expr` and watch the compiler point at every switch you must update (then remove it again).

</details>

<details><summary>Hint 4</summary>

`record` patterns bind components directly: `case Add(Expr left, Expr right)` - no casts, no accessor calls.

</details>
