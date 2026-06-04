# Task 03 — Input Types + Validation Clinic (Challenge)

## Summary

Upgrade a “broken intake” form to use **real HTML5 input types** and **constraint attributes**. Add buttons, validation UX styling, and explain why `novalidate` is present for this exercise.

## Learning goals

- Match input types to data shapes (`email`, `url`, `date`, `number`, `range`).
- Apply validation attributes with realistic bounds.

## Provided files

- `index.html`
- `styles/main.css`

## Prerequisites

- Day 12 theory sections on input types + constraint validation.

## What you will implement

Complete all `TODO(Day12-task03)` markers:

1. Add `submit` + `reset` controls with your own button labels.
2. Fix `email`, `url`, `date`, `number` fields per comments (include `autocomplete` on email).
3. Keep `range` bounds; add label hint + readout text per TODO comments.
4. Write footnote explaining `novalidate` on the `<form>`.

## Constraints

- No JavaScript.
- Do not remove the `<form>` element.

## Step-by-step guidance

1. Update types/attributes first; reload frequently.
2. Temporarily remove `novalidate` locally if you want to experience native submit blocking—**restore it before submitting** unless your instructor says otherwise.

## How to run and verify

### Manual checks

- [ ] Email field triggers basic email validation when `novalidate` is removed (demo only).
- [ ] Number field clamps/flags out-of-range per `min`/`max`.
- [ ] Date field restricts selectable window via `min`/`max`.
- [ ] Range thumb changes value (inspect `value` in DevTools after interaction).

## `TODO` map

| TODO | Done means |
|------|------------|
| Buttons | submit + reset exist with student labels |
| Inputs | Correct `type`s + required/min/max/step/autocomplete as specified |
| Range hint/readout | Visible instructions per TODO |
| Footnote | Explains `novalidate` purpose for this exercise |
| CSS | Valid/invalid styling approach implemented |

## Submission checklist (Git)

- [ ] `novalidate` remains on submitted form unless instructor directs otherwise

## Hints

<details><summary>`:user-invalid` support</summary>

If your browser does not show `:user-invalid`, still implement the selector block and document fallback in a CSS comment.

</details>
