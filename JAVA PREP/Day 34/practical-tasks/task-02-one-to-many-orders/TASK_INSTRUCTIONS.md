# Task 2 — One-to-Many: Customer and Orders

**Day:** 34 · **Task ID:** Day34-task02 · **Type:** Spring Boot · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Build a bidirectional one-to-many: mappedBy inverse side, owning many-to-one, sync helpers, cascade and orphanRemoval.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day34/task02/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day34/task02/Customer.java` | Stubs / starter code (edit the TODOs) |
| `src/main/java/com/javaprep/day34/task02/PurchaseOrder.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day34/task02/OneToManyTest.java` | Provided helper or test (do not edit) |
| `src/test/resources/application.properties` | Provided helper or test (do not edit) |

## Prerequisites

- Day 34 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Annotate `Customer.orders` (inverse side) and `PurchaseOrder.customer` (owning side).
2. Implement `addOrder`/`removeOrder` so both sides stay consistent.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day34-task02)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day34-task02)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 34: complete task-02-one-to-many-orders`.

## How to run and verify

```bash
java -version   # 21.x
mvn -v          # 3.9+
mvn test        # expected RED at the start
mvn -Dtest=<TestClass> test
```

## TODO map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `Customer.java` | `Day34-task02` | inverse side: mappedBy "customer", cascade ALL, orphanRemoval |
| `Customer.java` | `Day34-task02` | add to the list and set the back reference |
| `Customer.java` | `Day34-task02` | remove from the list and clear the back reference |
| `PurchaseOrder.java` | `Day34-task02` | owning side: many-to-one, LAZY, join column customer_id, not nullable |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `helpersKeepBothSidesInSync` |
| 2 | `persistCascadesToOrders` |
| 3 | `foreignKeyIsOnTheManySide` |
| 4 | `noJoinTableBecauseOfMappedBy` |
| 5 | `orphanRemovalDeletesRemovedOrder` |
| 6 | `removingCustomerRemovesOrders` |
| 7 | `manyToOneIsLazy` |

## Edge cases to handle

- Without `mappedBy` Hibernate invents a join table.
- `@ManyToOne` defaults to EAGER; set LAZY.
- orphanRemoval only triggers when the child is removed from the collection.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 34: One-to-Many: Customer and Orders`

## Hints (optional)

<details><summary>Hint 1</summary>
The side with the foreign key is the owning side.
</details>

<details><summary>Hint 2</summary>
Helpers are the only place that should touch both fields.
</details>
