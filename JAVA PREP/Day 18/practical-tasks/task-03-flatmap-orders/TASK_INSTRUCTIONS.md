# Task 3 — FlatMap Orders

**Day:** 18 · **Task ID:** Day18-task03 · **Type:** Plain Java · **Difficulty:** Stretch

## Summary

Flatten orders into line items with `flatMap` and compute analytics: distinct SKUs, units, revenue, units per SKU, the best-selling SKU, and words from sentences. Orders may have a `null` item list and must be treated as empty.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day18/task03/LineItem.java` | Provided type (no changes needed) |
| `src/main/java/com/javaprep/day18/task03/Order.java` | Provided type (no changes needed) |
| `src/main/java/com/javaprep/day18/task03/OrderAnalytics.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day18/task03/OrderAnalyticsTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 18 theory file read

## What you will implement

1. `allSkus(orders)` returns the distinct SKUs sorted alphabetically
2. `totalUnits(orders)` sums all line quantities (use a primitive stream)
3. `totalRevenue(orders)` sums `qty * price` over all lines
4. `unitsBySku(orders)` returns a `SortedMap<String,Integer>` of total units per SKU
5. `bestSellerSku(orders)` returns the SKU with most units as an `Optional` (ties: alphabetically first SKU); empty when there are no lines
6. `flattenWords(sentences)` splits sentences on whitespace into one list of words (blank sentences contribute nothing)
7. Orders whose `items` list is `null` are treated as having no items

## Constraints

- No explicit loops; `flatMap` must be used to flatten
- Do not edit the tests
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=OrderAnalyticsTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **7 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day18-task03)`).

### Run one test class

```bash
mvn -Dtest=OrderAnalyticsTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `OrderAnalytics.java` — `allSkus` | `TODO(Day18-task03)` | flatten to line items, map to sku, distinct, sorted |
| `OrderAnalytics.java` — `totalUnits` | `TODO(Day18-task03)` | flatten and sum qty with mapToInt |
| `OrderAnalytics.java` — `totalRevenue` | `TODO(Day18-task03)` | flatten and sum qty * price with mapToDouble |
| `OrderAnalytics.java` — `unitsBySku` | `TODO(Day18-task03)` | groupingBy(sku, TreeMap::new, summingInt(qty)) over the flattened lines |
| `OrderAnalytics.java` — `bestSellerSku` | `TODO(Day18-task03)` | the SKU with most units; ties -> alphabetically first; Optional.empty() when there are no lines |
| `OrderAnalytics.java` — `flattenWords` | `TODO(Day18-task03)` | flatMap each sentence to its whitespace-separated words, dropping empty tokens |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_allSkusDistinctSorted` |
| 2 | `r2_totalUnits` |
| 3 | `r3_totalRevenue` |
| 4 | `r4_unitsBySku` |
| 5 | `r5_bestSellerTieBreaksAlphabetically` |
| 6 | `r6_flattenWords` |
| 7 | `r7_nullItemListsAreEmpty` |

## Edge cases to handle

- null item list
- empty orders list
- ties for best seller
- blank sentences and multiple spaces

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 18: FlatMap Orders`

## Hints (optional)

<details><summary>Hint 1</summary>

Write one private helper that returns `Stream<LineItem>` and reuse it everywhere.

</details>

<details><summary>Hint 2</summary>

In the best-seller tie-break the *reversed* key comparator makes `max` pick the alphabetically first key.

</details>
