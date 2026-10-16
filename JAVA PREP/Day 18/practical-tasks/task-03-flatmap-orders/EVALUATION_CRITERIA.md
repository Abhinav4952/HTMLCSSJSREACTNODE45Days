# Evaluation Criteria — Day 18 — Task 03 — FlatMap Orders

## Scope

Graded: the behavior and quality of the implementation in `OrderAnalytics.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `allSkus(orders)` returns the distinct SKUs sorted alphabetically
- Requirement 2: `totalUnits(orders)` sums all line quantities (use a primitive stream)
- Requirement 3: `totalRevenue(orders)` sums `qty * price` over all lines
- Requirement 4: `unitsBySku(orders)` returns a `SortedMap<String,Integer>` of total units per SKU
- Requirement 5: `bestSellerSku(orders)` returns the SKU with most units as an `Optional` (ties: alphabetically first SKU); empty when there are no lines
- Requirement 6: `flattenWords(sentences)` splits sentences on whitespace into one list of words (blank sentences contribute nothing)
- Requirement 7: Orders whose `items` list is `null` are treated as having no items

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- null item list
- empty orders list
- ties for best seller
- blank sentences and multiple spaces

### Day-specific checks

- A single reusable flatMap helper
- Null item lists handled once, in the helper
- Primitive streams for numeric sums

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 18 Task 03 (FlatMap Orders) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `OrderAnalytics.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
