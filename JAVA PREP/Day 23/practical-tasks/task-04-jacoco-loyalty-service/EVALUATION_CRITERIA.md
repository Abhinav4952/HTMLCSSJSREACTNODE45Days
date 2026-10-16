# Evaluation Criteria — Day 23 — Task 04 — Coverage Challenge: Loyalty Service with Mockito and a Fixed Clock

## Scope

Graded: the behavior and quality of the implementation in `LoyaltyService.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `earn(customerId, spendCents)`: `spendCents <= 0` -> `IllegalArgumentException`; unknown customer -> `NoSuchElementException("unknown customer: <id>")`; points earned = `spendCents / 100 * tier.multiplier()`; new tier from the new total (`>= 1000` GOLD, `>= 500` SILVER, else BRONZE); `lastActivity` = today (from the injected `Clock`); the updated customer is saved once and returned
- Requirement 2: `redeem(customerId, points)`: `points <= 0` -> `IllegalArgumentException`; unknown customer -> `NoSuchElementException`; if the customer has been inactive for **more than 365 days** -> `IllegalStateException("points expired")`; not enough points -> `IllegalStateException("insufficient points")`; otherwise deduct, recompute the tier, set `lastActivity` to today, save, return
- Requirement 3: `expireInactive(ids)`: for each existing customer inactive for more than 365 days **and** holding points > 0, set points to 0 and tier to BRONZE and save; unknown ids and already-empty customers are skipped; returns the number of customers expired
- Requirement 4: `tierFor(points)` static helper implements the thresholds above

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- exactly 365 days of inactivity (not expired) vs 366
- tier boundaries 499/500/999/1000
- redeeming exactly all points
- unknown ids in `expireInactive`

### Day-specific checks

- Every branch of your implementation is exercised by the provided tests (JaCoCo branch coverage 100% on `LoyaltyService`)
- No hidden time dependency (`LocalDate.now()` without a clock)
- Repository is saved exactly when state changes

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`, JaCoCo summary (`target/site/jacoco/index.html`)

## AI-assisted grading prompt (optional)

```
You are grading Day 23 Task 04 (Coverage Challenge: Loyalty Service with Mockito and a Fixed Clock) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `LoyaltyService.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
