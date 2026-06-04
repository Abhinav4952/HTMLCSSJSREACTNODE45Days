# Task 02 — Fluid Type, `clamp()`, and Viewport Units

## Summary

Implement a responsive **article layout** where the **title**, **body**, and **section padding** scale fluidly using `clamp()` and at least one **`vw`-based** preferred expression. This task is meant to feel like tuning a real reading experience—not just copying one `clamp()` recipe.

## Learning goals

- Choose `MIN`/`MAX` bounds that keep body text readable on a 320px-wide viewport.
- Combine `rem` constants with `vw` slope in the preferred value.
- Use `min()` / `max()` at least once for layout width (optional but recommended).

## Provided files

- `index.html`
- `styles/main.css`

## Prerequisites

- Day 06 theory sections on `clamp()` and viewport units.

## What you will implement

Complete all `TODO(Day06-task02)` markers in `styles/main.css` (HTML is complete unless your instructor adds a TODO).

## Constraints

- Do not set body `font-size` below **15px** computed at 320px width (verify in DevTools after your clamp choices).
- Avoid `100vw` full-bleed hacks (they can introduce horizontal scroll).

## Step-by-step guidance

1. Start by setting `--step-0..--step-3` as a **modular scale** using `clamp()`.
2. Apply `--pad-x` to `article` and ensure line length stays comfortable (`max-width` already provided—don’t remove it).

## How to run and verify

### Manual checks

- [ ] At 320px width, no text feels “unreadably tiny.”
- [ ] At 1280px width, headline does not become absurdly huge unless `MAX` intentionally allows it within reason.

## `TODO` map

| TODO | Done means |
|------|------------|
| step variables | `--step-0`..`--step-3` defined with `clamp()` |
| typography | `h1`, `p`, `small` use those variables |
| padding | `--pad-x` uses `clamp()` with `vw` involvement |
| quote | `.pullquote` uses at least one `vw` term in `font-size` |

## Hints (tricky)

<details><summary>My clamp looks fine in Chrome but tiny in Safari iOS</summary>

Check minimum `rem` term: iOS can have different default text sizing; always include a solid `rem` baseline in the preferred expression, not `vw` alone.

</details>
