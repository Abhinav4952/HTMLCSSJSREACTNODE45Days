# Task 2 — Mockito: Order Service with Mocked Collaborators

**Day:** 23 · **Task ID:** Day23-task02 · **Type:** Plain Java · **Difficulty:** Core

## Summary

Implement `OrderService`, an order workflow orchestrating three collaborators (`InventoryClient`, `PaymentGateway`, `NotificationSender`). The tests use **Mockito** to stub outcomes, provoke gateway failures, capture notification messages, and verify call order and absence of interactions.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3, Mockito 5.14.2) |
| `src/main/java/com/javaprep/day23/task02/PaymentGateway.java` | Provided type (no changes needed) |
| `src/main/java/com/javaprep/day23/task02/InventoryClient.java` | Provided type (no changes needed) |
| `src/main/java/com/javaprep/day23/task02/NotificationSender.java` | Provided type (no changes needed) |
| `src/main/java/com/javaprep/day23/task02/OrderService.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day23/task02/OrderServiceTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 23 theory file read

## What you will implement

1. `placeOrder(customerId, sku, qty, unitPriceCents)` validates `qty > 0` and `unitPriceCents > 0` (otherwise `IllegalArgumentException` with **no** collaborator interaction)
2. It reserves stock; when `reserve` returns false the outcome is `OUT_OF_STOCK` and **neither payment nor notification** is touched
3. It charges `qty * unitPriceCents` (as `long`); an unsuccessful `PaymentResult` **or** a `RuntimeException` from the gateway releases the reserved stock, notifies `"Payment failed: <sku>"`, and returns `PAYMENT_FAILED`
4. On success it notifies `"Order confirmed: <sku> x<qty>"` and returns `CONFIRMED`; a `RuntimeException` thrown by the notifier is swallowed (the order stays confirmed)
5. `cancel(customerId, paymentId, sku, qty)` refunds the payment **first**, then releases the stock, then notifies `"Order cancelled: <sku>"`

## Constraints

- Constructor injection only; no static state; do not catch `Exception`/`Throwable` broadly (only `RuntimeException`)
- Do not edit the tests or the provided interfaces
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=OrderServiceTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **8 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day23-task02)`).

### Run one test class

```bash
mvn -Dtest=OrderServiceTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `OrderService.java` — `placeOrder` | `TODO(Day23-task02)` | validate qty/price (IAE, no calls); reserve; false -> OUT_OF_STOCK; charge qty*price in try/catch(RuntimeException); failure/decline -> release stock + notify "Payment failed: <sku>" + PAYMENT_FAILED; success -> notify "Order confirmed: <sku> x<qty>" (swallow RuntimeException from notifier) + CONFIRMED |
| `OrderService.java` — `cancel` | `TODO(Day23-task02)` | payments.refund(paymentId); inventory.release(sku, quantity); notify "Order cancelled: <sku>" (in exactly this order) |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_invalidInputTouchesNoCollaborator` |
| 2 | `r2_outOfStockDoesNotChargeOrNotify` |
| 3 | `r3_chargesQuantityTimesPriceAndConfirms`, `r3_declinedPaymentReleasesStockAndNotifies`, `r3_gatewayOutageIsTreatedAsPaymentFailure` |
| 4 | `r4_notificationFailureDoesNotUndoTheOrder`, `r4_stockIsReservedBeforeThePaymentIsTaken` |
| 5 | `r5_cancelRefundsThenReleasesThenNotifies` |

## Edge cases to handle

- reserve returns false
- gateway throws
- gateway declines
- notifier throws after a successful charge
- invalid quantity or price

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 23: Mockito: Order Service with Mocked Collaborators`

## Hints (optional)

<details><summary>Hint 1</summary>

Compute the amount as `(long) quantity * unitPriceCents` so large orders do not overflow `int`.

</details>

<details><summary>Hint 2</summary>

Treat a thrown `RuntimeException` from the gateway and a `success == false` result with the same compensation path.

</details>

<details><summary>Hint 3</summary>

Wrap the notification in its own try/catch - failing to notify must not roll back a paid order.

</details>
