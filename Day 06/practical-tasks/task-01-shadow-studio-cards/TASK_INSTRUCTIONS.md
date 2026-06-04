# Task 01 — Shadow Studio (Cards & Buttons)

## Summary

You will recreate a small **design-system-like** shadow ramp for cards and buttons using **layered `box-shadow`**, plus one tasteful **`text-shadow`** on a hero heading. This is the “confidence builder” task for Day 06.

## Learning goals

- Set comma-separated shadows for resting/hover states.
- Avoid “mud” by tuning blur vs alpha vs offset.

## Provided files

- `index.html` — marketing-ish layout with TODO hooks.
- `styles/main.css` — partial tokens; you complete shadows.

## Prerequisites

- Read Day 06 theory sections on `box-shadow` and `text-shadow`.

## What you will implement

1. Complete all `TODO(Day06-task01)` markers in CSS.
2. Ensure hover/focus-visible states are distinguishable without removing outlines.

## Constraints

- Do not use third-party CSS frameworks.
- Do not use `!important`.

## Step-by-step guidance

1. Fill `--shadow-*` variables first, then assign them to `.card` and `.card:hover`.
2. Add `text-shadow` only to `.hero-title` (not to body paragraphs).

## How to run and verify

### Install dependencies

None.

### Run tests

Not applicable.

### Manual checks

- [ ] Cards look elevated at rest and slightly more elevated on hover.
- [ ] Buttons have a subtle resting shadow and a deeper pressed (`:active`) inset feel.
- [ ] Hero title remains readable on the gradient background.

## `TODO` map

| TODO | Done means |
|------|------------|
| `--shadow-1..3` | Three distinct, non-identical shadow tokens |
| `.card` / hover | Uses tokens; hover increases elevation |
| `.btn` states | resting/hover/active shadows differ meaningfully |
| `.hero-title` | `text-shadow` improves contrast without huge blur |

## Submission checklist (Git)

- [ ] Intentional files only
- [ ] No secrets

## Hints (challenge extras)

<details><summary>Why does my shadow look “dirty”?</summary>

Lower alpha or reduce blur radius. Mud usually means blur is too large relative to offset and the rgba alpha is too high on a dark shadow over a mid background.

</details>
