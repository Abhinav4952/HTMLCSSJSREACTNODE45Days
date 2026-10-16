# Task 2 — Synchronized Bank Account and Safe Transfer

**Day:** 20 · **Task ID:** Day20-task02 · **Type:** Plain Java · **Difficulty:** Core

## Summary

Build a thread-safe `BankAccount` with validated `deposit`/`withdraw` and a `transfer` that is both atomic and **deadlock-free** by locking the two accounts in a global (id) order. The tests hammer the accounts from many threads, including opposing transfers, under a timeout.

## Learning goals

- Practice today's theory with a focused, testable API
- Drive the implementation from failing JUnit 5 + AssertJ tests
- Replace each `UnsupportedOperationException` stub with real behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5.11.4, AssertJ 3.27.3) |
| `src/main/java/com/javaprep/day20/task02/BankAccount.java` | Stubs with TODOs |
| `src/test/java/com/javaprep/day20/task02/BankAccountTest.java` | Specification tests (read-only) |

## Prerequisites

- Day 20 theory file read

## What you will implement

1. `BankAccount(id, initial)` rejects a negative initial balance with `IllegalArgumentException`
2. `deposit(amount)` and `withdraw(amount)` are thread-safe; non-positive amounts throw `IllegalArgumentException`; withdrawing more than the balance throws `IllegalStateException` and leaves the balance unchanged
3. `balance()` returns a consistent value even while other threads update the account
4. `transfer(from, to, amount)` moves money atomically; the sum of both balances is invariant; failure (insufficient funds) leaves both unchanged
5. `transfer` locks both accounts in ascending `id` order so `transfer(a,b)` and `transfer(b,a)` running concurrently never deadlock
6. `transfer` to the same account, or with a non-positive amount, throws `IllegalArgumentException`

## Constraints

- Use `synchronized` (no `java.util.concurrent.locks` yet)
- Do not edit the tests
- Java 21; no Docker; no external services; no Lombok

## Step-by-step guidance

1. Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).
2. Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.
3. Implement one TODO at a time, re-running `mvn -Dtest=BankAccountTest test` after each.
4. Refactor for clarity once green; re-run the full suite.
5. Commit with the message given in the submission checklist.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **8 tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day20-task02)`).

### Run one test class

```bash
mvn -Dtest=BankAccountTest test
```

### Manual checks

- [ ] No `UnsupportedOperationException` stubs remain on any path exercised by the tests
- [ ] Each public method has a one-line comment or self-explanatory name
- [ ] You can explain every line to a reviewer without referring to the tests

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
| `BankAccount.java` — `constructor` | `TODO(Day20-task02)` | store id and initialBalance; IllegalArgumentException when initialBalance is negative |
| `BankAccount.java` — `deposit` | `TODO(Day20-task02)` | IllegalArgumentException when amount <= 0; add to balance under this account's lock |
| `BankAccount.java` — `withdraw` | `TODO(Day20-task02)` | IllegalArgumentException when amount <= 0; IllegalStateException (balance unchanged) when amount > balance; subtract under the lock |
| `BankAccount.java` — `balance` | `TODO(Day20-task02)` | read balance under the same lock used by writers |
| `BankAccount.java` — `transfer` | `TODO(Day20-task02)` | validate (amount > 0, from != to by id) then lock the account with the smaller id first, then the other; withdraw from 'from' and deposit into 'to' while holding both locks |

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1 | `r1_constructorValidation` |
| 2 | `r2_depositAndWithdraw`, `r2_invalidAmountsAndInsufficientFunds` |
| 3 | `r3_concurrentDepositsAreNotLost` |
| 4 | `r4_transferMovesMoneyAtomically`, `r4_failedTransferChangesNothing` |
| 5 | `r5_opposingTransfersDoNotDeadlockAndKeepTheTotal` |
| 6 | `r6_invalidTransfers` |

## Edge cases to handle

- insufficient funds
- same-account transfer
- opposing concurrent transfers (deadlock test)
- validation before any locking side effects

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day 20: Synchronized Bank Account and Safe Transfer`

## Hints (optional)

<details><summary>Hint 1</summary>

Lock ordering needs a total order: the account id is perfect because it is unique and immutable.

</details>

<details><summary>Hint 2</summary>

`synchronized` is reentrant, so calling `withdraw`/`deposit` while already holding the lock is fine.

</details>
