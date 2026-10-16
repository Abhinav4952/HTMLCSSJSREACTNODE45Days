# Evaluation Criteria — Day 14 — Task 03 — Comparable Product Catalog

## Scope

Graded: the behavior and quality of the implementation in `Product.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: Constructor `Product(String sku, String name, long priceCents)` rejects a null/blank sku or null/blank name with `IllegalArgumentException` and a negative price with `IllegalArgumentException`
- Requirement 2: `compareTo` orders by `sku` ascending (use `String.compareTo`), never by subtraction
- Requirement 3: `equals`/`hashCode` depend on `sku` only, so they are consistent with `compareTo` (same sku -> `compareTo == 0` and `equals == true`)
- Requirement 4: `sku()`, `name()`, `priceCents()` accessors return the stored values (provided)
- Requirement 5: `TreeSet<Product>` de-duplicates by SKU, `Collections.sort` orders by SKU, and `Collections.max` returns the highest SKU

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- blank strings (`"   "`)
- price 0 allowed, -1 rejected
- same sku with different name/price is equal
- compareTo symmetry

### Day-specific checks

- `compareTo`, `equals`, `hashCode` use the same field(s)
- Immutability: all fields final, no setters
- Validation in one place (constructor)

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 14 Task 03 (Comparable Product Catalog) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `Product.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
