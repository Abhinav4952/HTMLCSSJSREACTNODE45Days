# Evaluation Criteria — Day 06 — Task 01 — Shadow Studio

## Scope

Graded: `styles/main.css` (primary) and any allowed HTML TODO completions in `index.html`.

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 45 | Shadows present; states differ; no layout breakage |
| Requirements coverage | 30 | TODO map satisfied |
| Code quality | 15 | Uses variables/tokens; readable values |
| UX / a11y | 10 | `:focus-visible` remains visible; hero title readable |

## Pass / fail gates

- `!important` used.
- Body paragraphs given large `text-shadow` blur (readability fail).

## Detailed rubric

### Correctness

- At least **two** comma-separated layers on `.card` OR one layer that is clearly intentional—not a random single huge blur.

### Edge cases

- Hover shadow should not clip awkwardly due to `overflow: hidden` on a parent—if it happens, candidate should adjust (minor).

## Evidence the grader should collect

- Screenshot at desktop + mobile width optional.

## AI grading prompt

Evaluate Day06 Task01 CSS: three shadow variables, card uses them with hover change, button resting/hover/active differ, hero title text-shadow subtle, focus-visible not removed.
