# Task 4 — Coverage Challenge: Loyalty Service with Mockito and a Fixed Clock

**Day:** 23 · **Task ID:** Day23-task04 · **Type:** Plain Java · **Difficulty:** Challenge

## Summary

Implement a branch-heavy `LoyaltyService` (points earning, tier changes, redemption, expiry). The tests combine **Mockito** (`@Mock` repository, `ArgumentCaptor` for saved customers) with an injected **fixed `Clock`**, and exercise every branch - after the tests are green, open the **JaCoCo** report and confirm your implementation has no uncovered branch.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3, Mockito 5.14.2) |
| `src/main/java/com/javaprep/day23/task04/CustomerRepository.java` | Provided type (no changes needed) |
| `src/main/java/com/javaprep/day23/task04/Customer.java` | Provided type (no changes needed) |
| `src/main/java/com/javaprep/day23/task04/LoyaltyService.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day23/task04/LoyaltyServiceTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 23 theory file read

## What you will implement

1. `earn(customerId, spendCents)`: `spendCents <= 0` -> `IllegalArgumentException`; unknown customer -> `NoSuchElementException("unknown customer: <id>")`; points earned = `spendCents / 100 * tier.multiplier()`; new tier from the new total (`>= 1000` GOLD, `>= 500` SILVER, else BRONZE); `lastActivity` = today (from the injected `Clock`); the updated customer is saved once and returned
2. `redeem(customerId, points)`: `points <= 0` -> `IllegalArgumentException`; unknown customer -> `NoSuchElementException`; if the customer has been inactive for **more than 365 days** -> `IllegalStateException("points expired")`; not enough points -> `IllegalStateException("insufficient points")`; otherwise deduct, recompute the tier, set `lastActivity` to today, save, return
3. `expireInactive(ids)`: for each existing customer inactive for more than 365 days **and** holding points > 0, set points to 0 and tier to BRONZE and save; unknown ids and already-empty customers are skipped; returns the number of customers expired
4. `tierFor(points)` static helper implements the thresholds above

## Constraints

- Use the injected `Clock`; no `LocalDate.now()` without it
- Do not edit the tests or the provided types
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=LoyaltyServiceTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **12 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day23-task04)`).

### Run one test class

```bash
mvn -Dtest=LoyaltyServiceTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `LoyaltyService.java` — `tierFor` | `TODO(Day23-task04)` | >= 1000 GOLD, >= 500 SILVER, otherwise BRONZE |
| `LoyaltyService.java` — `earn` | `TODO(Day23-task04)` | spend <= 0 -> IAE; load customer or NoSuchElementException("unknown customer: id"); earned = spend/100 * tier multiplier; save and return a copy with new points, tierFor(newPoints) and lastActivity = LocalDate.now(clock) |
| `LoyaltyService.java` — `redeem` | `TODO(Day23-task04)` | points <= 0 -> IAE; load customer; inactive > 365 days -> IllegalStateException("points expired"); points > balance -> IllegalStateException("insufficient points"); save and return the reduced customer with recomputed tier and lastActivity today |
| `LoyaltyService.java` — `expireInactive` | `TODO(Day23-task04)` | for every id: skip unknown customers, skip customers with 0 points or activity within 365 days; otherwise save points=0/BRONZE (lastActivity unchanged) and count it |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_tierThresholds` |
| 2 | `r2_earnUsesTheTierMultiplierAndUpdatesActivity`, `r2_goldEarnsTripleAndSilverDouble`, `r2_earnPromotesAcrossTierBoundaries`, `r2_earnRejectsInvalidInput` |
| 3 | `r3_redeemDeductsAndRecomputesTier`, `r3_redeemAllPointsIsAllowed`, `r3_redeemMoreThanBalanceFails`, `r3_exactly365DaysInactiveIsStillValidButOneMoreDayExpires`, `r3_redeemRejectsInvalidInput` |
| 4 | `r4_expireInactiveResetsOnlyStaleCustomersWithPoints`, `r4_expireInactiveWithNoIdsDoesNothing` |

## Edge cases to handle

- exactly 365 days of inactivity (not expired) vs 366
- tier boundaries 499/500/999/1000
- redeeming exactly all points
- unknown ids in `expireInactive`
- customers with zero points

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 23: Coverage Challenge: Loyalty Service with Mockito and a Fixed Clock`

## Hints (optional)

<details><summary>Hint 1</summary>

Keep the 365-day rule in one private helper so `redeem` and `expireInactive` agree on the boundary (`isBefore(today.minusDays(365))`).

</details>

<details><summary>Hint 2</summary>

`LocalDate.now(clock)` makes time injectable - never call `LocalDate.now()` without the clock.

</details>

<details><summary>Hint 3</summary>

After green: `mvn test`, then open `target/site/jacoco/index.html` and look for yellow/red diamonds.

</details>
