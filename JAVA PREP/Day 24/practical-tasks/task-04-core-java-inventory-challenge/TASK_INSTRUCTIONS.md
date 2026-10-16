# Task 4 — Core Java Capstone: Inventory Import and Report

**Day:** 24 · **Task ID:** Day24-task04 · **Type:** Plain Java · **Difficulty:** Challenge

## Summary

Pull the track together: validate data with a `record`, model parse outcomes with a sealed `ParseResult` (no exceptions escaping for bad lines), aggregate with streams and collectors, query with `Optional`, evict with a `LinkedHashMap`-based LRU cache, sum in parallel on **virtual threads**, and format a text report.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day24/task04/Item.java` | Stubs with TODOs |
| `src/main/java/com/javaprep/day24/task04/ParseResult.java` | Provided type (no changes needed) |
| `src/main/java/com/javaprep/day24/task04/LruCache.java` | Stubs with TODOs |
| `src/main/java/com/javaprep/day24/task04/InventoryReport.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day24/task04/InventoryReportTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 24 theory file read

## What you will implement

1. `Item` validation: `sku`/`category` non-blank (trimmed), `qty >= 0`, `priceCents >= 0`, otherwise `IllegalArgumentException` with a descriptive message; `valueCents()` is `qty * priceCents` as `long` (provided)
2. `InventoryReport.parseLine(lineNo, line)` splits `sku,category,qty,priceCents` (keeping empty fields) and returns `Ok(item)` or `Failed(lineNo, reason)` - reasons: `expected 4 fields but found N`, `invalid number: ...`, or the validation message; it never throws
3. `InventoryReport.parse(csv)` numbers lines from 1, skips blank lines, `#` comment lines, and a header line starting with `sku,`, and returns one `ParseResult` per remaining line in order
4. `valueByCategory(items)` returns a sorted map category -> total `valueCents`; `topN(items, n)` returns the `n` items with the highest value (ties by `sku`), `n < 0` -> `IllegalArgumentException`
5. `cheapestInStock(items, category)` returns the lowest-priced item of that category (case-insensitive) with `qty > 0`; ties by `sku`; empty `Optional` if none
6. `parallelTotal(items, batchSize)` sums `valueCents` of all items by splitting them into batches processed on a virtual-thread-per-task executor; `batchSize <= 0` -> `IllegalArgumentException`
7. `money(cents)` formats as `$1,234.56` (negative: `-$0.05`) and `render(totals)` prints one `name` + right-aligned money row per category (name left-aligned in 10 chars, one space, money right-aligned in 10) followed by a `TOTAL` row
8. `LruCache<K,V>(capacity)`: `get` (null when absent, marks as recently used), `put`, `size`, `keys()` eldest to newest; capacity <= 0 -> `IllegalArgumentException`; the eldest entry is evicted when capacity is exceeded

## Constraints

- Use records and the sealed `ParseResult`; do not return `null` for missing values (use `Optional`)
- No parallel streams: use virtual threads for `parallelTotal`
- Do not edit the tests or `ParseResult`
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=InventoryReportTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **17 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day24-task04)`).

### Run one test class

```bash
mvn -Dtest=InventoryReportTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `Item.java` — `validation` | `TODO(Day24-task04)` | sku and category must be non-null and non-blank (IllegalArgumentException with a message naming the field); qty >= 0; priceCents >= 0; store the trimmed sku and category |
| `LruCache.java` — `constructor` | `TODO(Day24-task04)` | capacity <= 0 -> IllegalArgumentException; create new LinkedHashMap<>(16, 0.75f, true) overriding removeEldestEntry to evict when size() > capacity |
| `LruCache.java` — `get` | `TODO(Day24-task04)` | return map.get(key) (null when absent); access order makes it the most recently used |
| `LruCache.java` — `put` | `TODO(Day24-task04)` | map.put(key, value); an overwrite also refreshes the key |
| `LruCache.java` — `keys` | `TODO(Day24-task04)` | a new ArrayList of the key set: eldest (least recently used) first |
| `InventoryReport.java` — `parseLine` | `TODO(Day24-task04)` | split(",", -1); length != 4 -> Failed(line, "expected 4 fields but found N"); parse qty (int) and priceCents (long) - NumberFormatException -> Failed(line, "invalid number: " + message); IllegalArgumentException from Item -> Failed(line, its message); success -> Ok(item); never throw |
| `InventoryReport.java` — `parse` | `TODO(Day24-task04)` | iterate csv.lines() with a 1-based counter; skip blank lines, lines starting with # and a header starting with "sku,"; every other line becomes parseLine(counter, line); null csv -> empty list |
| `InventoryReport.java` — `valueByCategory` | `TODO(Day24-task04)` | Collectors.groupingBy(Item::category, TreeMap::new, Collectors.summingLong(Item::valueCents)) |
| `InventoryReport.java` — `topN` | `TODO(Day24-task04)` | n < 0 -> IllegalArgumentException; sort by valueCents descending then sku ascending; limit(n); toList() |
| `InventoryReport.java` — `cheapestInStock` | `TODO(Day24-task04)` | filter category equalsIgnoreCase and qty > 0; min by priceCents then sku |
| `InventoryReport.java` — `parallelTotal` | `TODO(Day24-task04)` | batchSize <= 0 -> IllegalArgumentException; split into subList batches; try-with-resources Executors.newVirtualThreadPerTaskExecutor(); submit one Callable<Long> per batch; add up future.get(); wrap ExecutionException in IllegalStateException and restore the interrupt flag on InterruptedException |
| `InventoryReport.java` — `money` | `TODO(Day24-task04)` | "$" + dollars with thousands separators (Locale.ROOT, ",") + "." + two-digit cents; negative values get a leading "-" before the "$" |
| `InventoryReport.java` — `render` | `TODO(Day24-task04)` | one row per entry in map order: String.format(Locale.ROOT, "%-10s %10s", name, money(value)); then a last row "TOTAL" with the sum; rows joined with \n (no trailing newline) |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_itemTrimsAndComputesValue`, `r1_itemValidation` |
| 2 | `r2_parseLineSuccess`, `r2_parseLineFailuresNeverThrow`, `r2_parseSkipsNoiseAndNumbersPhysicalLines`, `r2_parseHandlesEmptyInput` |
| 3 | `r3_valueByCategoryIsSorted`, `r3_topNOrdersByValueThenSku`, `r3_cheapestInStockIgnoresEmptyShelvesAndCase` |
| 4 | `r4_parallelTotalMatchesSequentialSum`, `r4_parallelTotalRejectsBadBatchSize` |
| 5 | `r5_renderTable`, `r5_endToEnd` |
| 6 | `r6_evictsTheLeastRecentlyUsedEntry`, `r6_overwritingRefreshesAndKeepsSize`, `r6_keysReturnsASnapshot`, `r6_invalidCapacity` |

## Edge cases to handle

- blank lines, comments, header
- line with too many/few fields
- non-numeric and negative quantities
- zero-quantity items for `cheapestInStock`
- empty collections
- LRU refresh on `get` and on overwriting `put`

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 24: Core Java Capstone: Inventory Import and Report`

## Hints (optional)

<details><summary>Hint 1</summary>

Parse in two layers: `parseLine` turns *any* string into a `ParseResult`; `parse` only handles line numbering and skipping.

</details>

<details><summary>Hint 2</summary>

`Collectors.groupingBy(classifier, TreeMap::new, downstream)` gives you a sorted map directly.

</details>

<details><summary>Hint 3</summary>

For `parallelTotal`, submit batches to `Executors.newVirtualThreadPerTaskExecutor()` in a try-with-resources; `subList` views are fine to read from several threads because nothing mutates the list.

</details>

<details><summary>Hint 4</summary>

`Comparator.comparingLong(Item::valueCents).reversed().thenComparing(Item::sku)` - reversal applies only to what came before it.

</details>
