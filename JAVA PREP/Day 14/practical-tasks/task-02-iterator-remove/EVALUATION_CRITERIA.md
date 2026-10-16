# Evaluation Criteria — Day 14 — Task 02 — Iterator Removal Lab

## Scope

Graded: the behavior and quality of the implementation in `IteratorOps.java` against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

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

- Requirement 1: `removeNegatives(List<Integer>)` removes negative values **in place** using `Iterator.remove()` and returns how many were removed
- Requirement 2: `removeMatching(Collection<T>, Predicate<? super T>)` removes matching elements in place and returns the count (use an iterator, not `removeIf`)
- Requirement 3: `duplicateEvens(List<Integer>)` inserts a copy right after each even number using `ListIterator.add`
- Requirement 4: `forEachRemovalThrows(input, toRemove)` copies the list, removes `toRemove` inside a for-each loop, and returns `true` if `ConcurrentModificationException` was thrown, else `false`

### Code quality

- Names express intent; methods stay short and single-purpose
- No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)
- No unnecessary raw types, casts, or `@SuppressWarnings` without a comment

### Robustness & safety

- empty collection
- all elements match / none match
- `LinkedList` and `ArrayList` both supported
- removing the second-to-last element does not throw

### Day-specific checks

- Mutation happens through the iterator, never through the collection
- `removeIf` not used where the task demands an explicit iterator
- Explains the silent second-to-last case in a short comment

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`

## AI-assisted grading prompt (optional)

```
You are grading Day 14 Task 02 (Iterator Removal Lab) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review `IteratorOps.java` for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
