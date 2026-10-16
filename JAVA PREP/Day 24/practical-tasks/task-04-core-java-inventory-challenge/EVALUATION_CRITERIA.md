# Evaluation Criteria — Day 24 — Task 04 — Core Java Capstone: Inventory Import and Report

## Scope

Graded: the behavior and quality of the implementation in `Item.java`, `LruCache.java`, `InventoryReport.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `Item` validation: `sku`/`category` non-blank (trimmed), `qty >= 0`, `priceCents >= 0`, otherwise `IllegalArgumentException` with a descriptive message; `valueCents()` is `qty * priceCents` as `long` (provided)
- Requirement 2: `InventoryReport.parseLine(lineNo, line)` splits `sku,category,qty,priceCents` (keeping empty fields) and returns `Ok(item)` or `Failed(lineNo, reason)` - reasons: `expected 4 fields but found N`, `invalid number: ...`, or the validation message; it never throws
- Requirement 3: `InventoryReport.parse(csv)` numbers lines from 1, skips blank lines, `#` comment lines, and a header line starting with `sku,`, and returns one `ParseResult` per remaining line in order
- Requirement 4: `valueByCategory(items)` returns a sorted map category -> total `valueCents`; `topN(items, n)` returns the `n` items with the highest value (ties by `sku`), `n < 0` -> `IllegalArgumentException`
- Requirement 5: `cheapestInStock(items, category)` returns the lowest-priced item of that category (case-insensitive) with `qty > 0`; ties by `sku`; empty `Optional` if none
- Requirement 6: `parallelTotal(items, batchSize)` sums `valueCents` of all items by splitting them into batches processed on a virtual-thread-per-task executor; `batchSize <= 0` -> `IllegalArgumentException`
- Requirement 7: `money(cents)` formats as `$1,234.56` (negative: `-$0.05`) and `render(totals)` prints one `name` + right-aligned money row per category (name left-aligned in 10 chars, one space, money right-aligned in 10) followed by a `TOTAL` row
- Requirement 8: `LruCache<K,V>(capacity)`: `get` (null when absent, marks as recently used), `put`, `size`, `keys()` eldest to newest; capacity <= 0 -> `IllegalArgumentException`; the eldest entry is evicted when capacity is exceeded

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- blank lines, comments, header
- line with too many/few fields
- non-numeric and negative quantities
- zero-quantity items for `cheapestInStock`

### Day-specific checks

- Bad input never throws out of `parseLine`/`parse`
- Immutable data (records) and unmodifiable results; no shared mutable state in the parallel code
- Streams used for aggregation but loops where they are clearer
- No resource leaks (executor closed, interrupt flag restored)

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`, JaCoCo summary (`target/site/jacoco/index.html`)

## AI-assisted grading prompt (optional)

```
You are grading Day 24 Task 04 (Core Java Capstone: Inventory Import and Report) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `Item.java`, `LruCache.java`, `InventoryReport.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
