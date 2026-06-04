# Evaluation Criteria — Day 08 — Task 03 — Fixed + Sticky Shell

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 65 | Header fixed; sticky works inside scrollport |
| UX / a11y | 20 | Content remains reachable; no accidental clipping |
| Code quality | 15 | Clear structure |

## Pass / fail gates

- Sticky never engages due to `overflow: hidden` misuse on wrong ancestor (if introduced by candidate).
