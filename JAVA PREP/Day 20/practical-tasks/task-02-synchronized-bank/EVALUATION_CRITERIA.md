# Evaluation Criteria — Day 20 — Task 02 — Synchronized Bank Account and Safe Transfer

## Scope

Graded: the behavior and quality of the implementation in `BankAccount.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `BankAccount(id, initial)` rejects a negative initial balance with `IllegalArgumentException`
- Requirement 2: `deposit(amount)` and `withdraw(amount)` are thread-safe; non-positive amounts throw `IllegalArgumentException`; withdrawing more than the balance throws `IllegalStateException` and leaves the balance unchanged
- Requirement 3: `balance()` returns a consistent value even while other threads update the account
- Requirement 4: `transfer(from, to, amount)` moves money atomically; the sum of both balances is invariant; failure (insufficient funds) leaves both unchanged
- Requirement 5: `transfer` locks both accounts in ascending `id` order so `transfer(a,b)` and `transfer(b,a)` running concurrently never deadlock
- Requirement 6: `transfer` to the same account, or with a non-positive amount, throws `IllegalArgumentException`

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- insufficient funds
- same-account transfer
- opposing concurrent transfers (deadlock test)
- validation before any locking side effects

### Day-specific checks

- Same lock discipline for reads and writes
- Lock ordering by id explained in a comment
- No `Thread.sleep` or retry loops to "avoid" deadlock

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 20 Task 02 (Synchronized Bank Account and Safe Transfer) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `BankAccount.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
