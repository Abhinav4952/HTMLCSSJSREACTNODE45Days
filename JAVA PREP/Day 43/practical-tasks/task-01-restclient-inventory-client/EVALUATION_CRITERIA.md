# Evaluation Criteria — Day 43 — Task 01 — RestClient Inventory Client

## Scope

Automated JUnit verification plus light code/SQL quality review for Day 43 Task 01 (`restclient-inventory-client`).

## Weighting (100 points)

| Category | Points |
|----------|-------:|
| Correctness (all tests green, requirements met) | 60 |
| Edge cases and error contracts | 20 |
| Code clarity (naming, simplicity, idiomatic Spring/SQL) | 15 |
| Git / hygiene (no `target/`, no secrets, only intended files changed) | 5 |

## Pass / fail gates (automatic fail if violated)

- Project does not compile or `mvn test` fails
- Tests, `pom.xml`, or provided helpers modified to force a pass
- Hard-coded answers that special-case test inputs
- Secrets or `target/` committed

## Detailed rubric

### Correctness

- Implement `availableStock(sku)` with `restClient.get().uri("/inventory/{sku}", sku)`.
- Return the `available` count wrapped in `Optional` for 200 responses.
- Return `Optional.empty()` for HTTP 404.
- Throw `InventoryUnavailableException` for 5xx responses and for I/O failures (`ResourceAccessException`).
- Use a URI template variable so the SKU is encoded for you (never concatenate strings).

### Edge cases

- SKU containing a space must be percent-encoded.
- A 4xx other than 404 may propagate (document your choice).
- Keep the original exception as `cause`.

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day43-task01)`

## AI grading prompt (paste into your grader)

```
You are grading Day 43 Task 01 (RestClient Inventory Client) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
