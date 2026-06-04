# Evaluation Criteria — Day 01 — Task 02 — Head Metadata Basics

## Scope

Graded: `index.html` metadata additions; `assets/favicon.svg` should remain a valid SVG (unchanged unless instructed).

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 40 | Valid tags; favicon path resolves; charset/viewport/title still sensible |
| Requirements coverage | 35 | Author, description length band, theme-color, favicon link |
| Code quality | 15 | Consistent formatting; no duplicate conflicting meta |
| Docs / readability | 10 | Description is readable English (or instructor-approved language) |

## Pass / fail gates

- Missing `charset` or `viewport` if removed by candidate.
- Description outside **120–180** characters after trimming whitespace.
- Favicon `href` clearly broken (404 when served from task folder root).

## Detailed rubric

### Correctness

- Icon link uses correct relative path from `index.html` location.
- Theme color is a valid CSS color token (hex preferred).

### Edge cases

- Extremely long author strings—acceptable if not abusive; cap at ~120 chars for author if needed for policy.

### UX / accessibility

- Description should not be keyword-stuffed nonsense.

## Evidence the grader should collect

- Character count proof for description (selection screenshot or note).

## AI grading prompt (paste into your grader)

Evaluate Day 01 Task 02. Inspect `index.html` for author meta, description meta with length 120–180 inclusive, theme-color meta, link rel=icon to assets/favicon.svg. Confirm charset/viewport/title still appropriate. Return Pass/Fail, score table, blocking issues.
