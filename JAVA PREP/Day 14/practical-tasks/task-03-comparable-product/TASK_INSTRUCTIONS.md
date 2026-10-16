# Task 3 — Comparable Product Catalog

**Day:** 14 · **Task ID:** Day14-task03 · **Type:** Plain Java · **Difficulty:** Core

## Summary

Create a `Product` value class whose natural order is its SKU, whose `equals`/`hashCode` are consistent with that order, and whose constructor validates its inputs. The tests sort lists, use a `TreeSet`, and check consistency with `equals`.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day14/task03/Product.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day14/task03/ProductTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 14 theory file read

## What you will implement

1. Constructor `Product(String sku, String name, long priceCents)` rejects a null/blank sku or null/blank name with `IllegalArgumentException` and a negative price with `IllegalArgumentException`
2. `compareTo` orders by `sku` ascending (use `String.compareTo`), never by subtraction
3. `equals`/`hashCode` depend on `sku` only, so they are consistent with `compareTo` (same sku -> `compareTo == 0` and `equals == true`)
4. `sku()`, `name()`, `priceCents()` accessors return the stored values (provided)
5. `TreeSet<Product>` de-duplicates by SKU, `Collections.sort` orders by SKU, and `Collections.max` returns the highest SKU

## Constraints

- Do not edit the tests; do not hard-code expected values
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=ProductTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **6 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day14-task03)`).

### Run one test class

```bash
mvn -Dtest=ProductTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `Product.java` — `constructor` | `TODO(Day14-task03)` | validate (blank/null sku or name, negative price -> IllegalArgumentException) then store the fields |
| `Product.java` — `compareTo` | `TODO(Day14-task03)` | compare by sku using String.compareTo (no subtraction); must be consistent with equals |
| `Product.java` — `equals` | `TODO(Day14-task03)` | equal when the other object is a Product with the same sku |
| `Product.java` — `hashCode` | `TODO(Day14-task03)` | derive from sku only |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_constructorStoresValues`, `r1_constructorValidation` |
| 2 | `r2_compareToOrdersBySku` |
| 3 | `r3_equalsAndHashCodeUseSkuOnly`, `r3_consistentWithEqualsForAllPairs` |
| 5 | `r5_sortingAndTreeSet` |

## Edge cases to handle

- blank strings (`"   "`)
- price 0 allowed, -1 rejected
- same sku with different name/price is equal
- compareTo symmetry

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 14: Comparable Product Catalog`

## Hints (optional)

<details><summary>Hint 1</summary>

`compareTo` on strings already returns a signed int; do not negate or subtract.

</details>

<details><summary>Hint 2</summary>

Remember `Objects.hash(sku)` or `sku.hashCode()` - both fine.

</details>
