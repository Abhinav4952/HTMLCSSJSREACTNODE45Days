# Task 2 — @Transactional: Atomic Transfer and Rollback Rules

**Day:** 35 · **Task ID:** Day35-task02 · **Type:** Spring Boot · **Difficulty:** Core

> Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds.

## Summary

Make a money transfer atomic with @Transactional and learn that checked exceptions need rollbackFor.

## Learning goals

- Apply today's theory to a small, testable problem
- Drive the work from failing tests (`mvn test`)
- Replace stubs/TODO markers with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
| `src/main/java/com/javaprep/day35/task02/Application.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day35/task02/BankAccount.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day35/task02/BankAccountRepository.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day35/task02/InsufficientFundsException.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day35/task02/AuditUnavailableException.java` | Provided helper or test (do not edit) |
| `src/main/java/com/javaprep/day35/task02/TransferService.java` | Stubs / starter code (edit the TODOs) |
| `src/test/java/com/javaprep/day35/task02/TransferServiceTest.java` | Provided helper or test (do not edit) |
| `src/test/resources/application.properties` | Provided helper or test (do not edit) |

## Prerequisites

- Day 35 theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

1. Add `@Transactional` to `transfer`, `@Transactional(rollbackFor=...)` to `transferWithAudit`, `readOnly` to `balanceOf`.
2. Implement the three method bodies.

## Constraints

- Java 21; Spring Boot 3.4.1 starters already declared in `pom.xml`; no Lombok; do not add dependencies.
- Do not edit test files or this document; edit only the places marked `TODO(Day35-task02)`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day35-task02)` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day 35: complete task-02-transactional-transfer`.

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
| `TransferService.java` | `Day35-task02` | make this method run in a transaction |
| `TransferService.java` | `Day35-task02` | implement steps 1-3 |
| `TransferService.java` | `Day35-task02` | transactional, rolling back for the CHECKED exception too (rollbackFor |
| `TransferService.java` | `Day35-task02` | call transfer logic (not through a proxy: inline the steps or call this.transfer) then throw AuditUnavailableException |
| `TransferService.java` | `Day35-task02` | read-only transaction |
| `TransferService.java` | `Day35-task02` | return the balance |

## Test map

| # | Test method |
|--:|-------------|
| 1 | `setUp` |
| 2 | `successfulTransferMovesMoney` |
| 3 | `insufficientFundsChangesNothing` |
| 4 | `failureAfterDebitRollsEverythingBack` |
| 5 | `checkedExceptionRollsBackBecauseOfRollbackFor` |
| 6 | `unknownAccountBalanceThrows` |

## Edge cases to handle

- `RuntimeException`/`Error` roll back by default; checked exceptions do not.
- Self-invocation (`this.transfer`) bypasses the proxy: the outer annotation must carry the transaction.

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day 35: @Transactional: Atomic Transfer and Rollback Rules`

## Hints (optional)

<details><summary>Hint 1</summary>
`saveAndFlush` makes the debit visible to the database inside the transaction - and proves rollback.
</details>

<details><summary>Hint 2</summary>
Tests deliberately are not `@Transactional`; otherwise the test transaction would hide the behavior.
</details>
