# Task 3 — CompletableFuture Pipeline

**Day:** 21 · **Task ID:** Day21-task03 · **Type:** Plain Java · **Difficulty:** Stretch

## Summary

Compose asynchronous work with `CompletableFuture`: a transform pipeline, combining two results, collecting a list of futures in order, a fallback on failure, dependent calls with `thenCompose`, a default-on-timeout, and a `describe` function that unwraps `CompletionException`.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day21/task03/CompletablePipeline.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day21/task03/CompletablePipelineTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 21 theory file read

## What you will implement

1. `pipeline(source, executor)` runs `source` asynchronously on `executor`, trims the text, then upper-cases it
2. `combine(a, b)` completes with the sum of both results (`thenCombine`)
3. `allInOrder(futures)` completes with the list of all results in the **input order** (`allOf` + `join`)
4. `withFallback(risky, executor, fallback)` runs `risky` asynchronously and completes with `fallback` if it throws
5. `chain(id, lookupUser, lookupEmail)` runs `lookupUser(id)` then `lookupEmail(user)` using `thenCompose`
6. `withTimeout(future, millis, defaultValue)` completes with `defaultValue` when the future is not done in time (`completeOnTimeout`)
7. `describe(future)` returns `"ok:<value>"` or `"error:<root exception simple name>"`, unwrapping a `CompletionException`

## Constraints

- Return `CompletableFuture`s - do not block the calling thread in any method
- Do not edit the tests
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=CompletablePipelineTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **11 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day21-task03)`).

### Run one test class

```bash
mvn -Dtest=CompletablePipelineTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `CompletablePipeline.java` — `pipeline` | `TODO(Day21-task03)` | supplyAsync(source, executor) then thenApply(trim) then thenApply(toUpperCase) |
| `CompletablePipeline.java` — `combine` | `TODO(Day21-task03)` | a.thenCombine(b, Integer::sum) |
| `CompletablePipeline.java` — `allInOrder` | `TODO(Day21-task03)` | CompletableFuture.allOf(...) then collect each future's join() preserving the input order (empty list gives an already completed empty result) |
| `CompletablePipeline.java` — `withFallback` | `TODO(Day21-task03)` | supplyAsync(risky, executor).exceptionally(ex -> fallback) |
| `CompletablePipeline.java` — `chain` | `TODO(Day21-task03)` | lookupUser.apply(id) then thenCompose(lookupEmail) - NOT thenApply (that would nest futures) |
| `CompletablePipeline.java` — `withTimeout` | `TODO(Day21-task03)` | future.completeOnTimeout(defaultValue, millis, MILLISECONDS) |
| `CompletablePipeline.java` — `describe` | `TODO(Day21-task03)` | handle((value, ex) -> ...): "ok:<value>" or "error:<SimpleName of the root exception>" unwrapping CompletionException |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_pipelineTransformsText`, `r1_pipelinePropagatesSourceFailure` |
| 2 | `r2_combineSums`, `r2_combineWaitsForBoth` |
| 3 | `r3_allInOrderKeepsInputOrder`, `r3_allInOrderEmpty` |
| 4 | `r4_fallbackOnFailureAndNoFallbackOnSuccess` |
| 5 | `r5_chainComposesDependentCalls`, `r5_chainFailsWhenFirstLookupFails` |
| 6 | `r6_timeoutUsesTheDefault` |
| 7 | `r7_describeUnwrapsCompletionException` |

## Edge cases to handle

- failure in the middle of a chain
- future that never completes
- empty list in `allInOrder`
- wrapped vs direct exceptions in `describe`

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 21: CompletableFuture Pipeline`

## Hints (optional)

<details><summary>Hint 1</summary>

`allOf` returns `CompletableFuture<Void>`: gather results in a `thenApply` after it completes (calling `join()` there never blocks).

</details>

<details><summary>Hint 2</summary>

A failed derived stage hands `handle` a `CompletionException`; a directly failed future does not.

</details>
