# Evaluation Criteria — Day 01 — Task 03 — External Assets, defer, async

## Scope

Graded: `index.html` wiring for CSS/JS; no changes required inside provided JS unless TODOs appear there (default: none).

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 50 | No console errors; deferred script reads `#greeting` text successfully |
| Requirements coverage | 30 | Correct `rel`/`href` for CSS; correct `async`/`defer` usage per instructions |
| Code quality | 10 | Script tags ordered sensibly; no duplicate loads |
| Docs / readability | 10 | If candidate adds brief HTML comment explaining order, reward clarity |

## Pass / fail gates

- Uncaught exception from `app-deferred.js`.
- Stylesheet not linked; page obviously unstyled.
- `app-deferred.js` loaded without `defer` while still relying on early DOM (if that breaks acceptance substring).

## Detailed rubric

### Correctness

- Console must contain substring: `deferred app sees: Hello from Day 01 task 03`.

### Edge cases

- Hard refresh should behave the same; if intermittent race from `async` helper, acceptable unless it throws.

## Evidence the grader should collect

- Screenshot or copy/paste of console lines.
- Browser name + version optional.

## AI grading prompt (paste into your grader)

Evaluate Day 01 Task 03. Check index.html for link to styles/main.css; three script tags with correct src paths; helper-async.js has async; app-deferred.js has defer; acceptance console substring present conceptually (candidate describes result). Flag any TypeErrors.
