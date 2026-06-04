# Task 04 — Constraint Validation UX Patterns

## Summary

Polish a constrained username field: human-readable help text, a visible **error message** surfaced without JavaScript using modern CSS pseudo-classes where possible, and strong focus styles.

## Learning goals

- Tie `pattern`, `minlength`, and `maxlength` to user-facing guidance.
- Use `:user-invalid` / `:user-valid` with honest fallbacks.

## Provided files

- `index.html`
- `styles/main.css`

## Prerequisites

- Task 03 + Day 12 theory.

## What you will implement

1. Complete all `TODO(Day12-task04)` markers.
2. Help text must describe the real rules enforced by `pattern` + lengths.
3. Error message paragraph contains short friendly text and is shown/hidden via CSS per instructions in `main.css` TODO block (no JS).

## Constraints

- No JavaScript.
- Do not loosen the `pattern` without updating help text accordingly.

## Step-by-step guidance

1. Write help text first; only then tweak copy to match regex semantics.
2. Implement `:has()` + `:user-invalid` visibility pattern; document fallback.

## How to run and verify

### Manual checks

- [ ] Typing `A` at start shows invalid state after interaction rules of `:user-invalid` (may require blur/submit depending on browser).
- [ ] Valid handle like `ada_lovelace` does not show the error state.
- [ ] Focus rings are obvious on keyboard navigation.

## `TODO` map

| TODO | Done means |
|------|------------|
| Help text | Matches pattern + lengths |
| Error text | Friendly message present |
| CSS | Error visibility rules + borders + focus-visible |

## Submission checklist (Git)

- [ ] TODOs removed

## Hints

<details><summary>`:user-invalid` behavior</summary>

Browsers differ on when `:user-invalid` activates. Your rubric allows documenting the chosen browser for demo.

</details>
