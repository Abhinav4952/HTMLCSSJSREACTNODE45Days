# Evaluation Criteria — Day 23 — Task 02 — Mockito: Order Service with Mocked Collaborators

## Scope

Graded: the behavior and quality of the implementation in `OrderService.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `placeOrder(customerId, sku, qty, unitPriceCents)` validates `qty > 0` and `unitPriceCents > 0` (otherwise `IllegalArgumentException` with **no** collaborator interaction)
- Requirement 2: It reserves stock; when `reserve` returns false the outcome is `OUT_OF_STOCK` and **neither payment nor notification** is touched
- Requirement 3: It charges `qty * unitPriceCents` (as `long`); an unsuccessful `PaymentResult` **or** a `RuntimeException` from the gateway releases the reserved stock, notifies `"Payment failed: <sku>"`, and returns `PAYMENT_FAILED`
- Requirement 4: On success it notifies `"Order confirmed: <sku> x<qty>"` and returns `CONFIRMED`; a `RuntimeException` thrown by the notifier is swallowed (the order stays confirmed)
- Requirement 5: `cancel(customerId, paymentId, sku, qty)` refunds the payment **first**, then releases the stock, then notifies `"Order cancelled: <sku>"`

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- reserve returns false
- gateway throws
- gateway declines
- notifier throws after a successful charge

### Day-specific checks

- Compensation (release stock) happens on every failure path after reserve
- No collaborator calls on validation failure or out-of-stock
- Order of side effects is deliberate and tested

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`, JaCoCo summary (`target/site/jacoco/index.html`)

## AI-assisted grading prompt (optional)

```
You are grading Day 23 Task 02 (Mockito: Order Service with Mocked Collaborators) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `OrderService.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
