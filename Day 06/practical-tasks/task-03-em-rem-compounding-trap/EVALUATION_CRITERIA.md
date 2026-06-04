# Evaluation Criteria — Day 06 — Task 03 — em/rem Compounding Trap

## Scope

Graded: `styles/main.css` only; `index.html` must remain unchanged (byte-for-byte unless whitespace policy says otherwise—default: unchanged).

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 55 | Meets acceptance checklist; no runaway compounding |
| Requirements coverage | 25 | TODO map satisfied |
| Code quality | 20 | Explains approach in CSS comments at top (3–8 lines) |
| UX / a11y | 10 | Readable hierarchy; focus styles preserved |

## Pass / fail gates

- `index.html` modified (automatic fail unless instructor override).
- Depth-3 `.chip` computed font-size > 20% different from depth-1 `.chip` (too much compounding remains).

## Evidence the grader should collect

- DevTools computed `font-size` for `.chip` at depth 1 vs depth 3.
- Computed padding totals for `.chip` at depth 1 vs depth 3.

## AI grading prompt

Confirm index.html unchanged. Inspect CSS: nested module strategy avoids em font-size compounding; chips stable; comment explains rationale. Compare computed sizes conceptually from candidate notes.
