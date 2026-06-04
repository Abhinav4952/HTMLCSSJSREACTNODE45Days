# Task 02 — Breakpoint Padding Footgun Clinic (Challenge)

## Summary

A “helpful” breakpoint adds **inline padding** to a full-bleed band that already contains a **3-column CSS grid**. Your job is to eliminate the **horizontal scrollbar** while keeping the design intent (more air at larger widths).

## Learning goals

- Debug overflow caused by **padding + percent/fr tracks + gaps**.
- Explain the fix in one sentence (HTML lede TODO).

## Provided files

- `index.html`
- `styles/main.css`

## Prerequisites

- Day 13 theory: breakpoint footguns.

## What you will implement

1. Fix overflow per CSS TODO (document strategy in a CSS comment).
2. Add the second breakpoint tightening rules.
3. Complete lede sentence in HTML.

## Constraints

- No JavaScript.
- Keep three columns at `min-width: 720px` (do not collapse to one column to “cheat” unless you document a product reason—preferred: keep 3 columns).

## How to run and verify

### Manual checks

- [ ] Resize from 360px wide to 1400px: **no persistent horizontal scrollbar** from `.band` layout (vertical scroll OK).
- [ ] At ≥1100px, gap increases subtly per TODO.

## `TODO` map

| TODO | Done means |
|------|------------|
| CSS footgun fix | Documented strategy; overflow resolved |
| CSS second breakpoint | Gap rule added |
| HTML lede | Explains fix briefly |

## Submission checklist (Git)

- [ ] TODOs removed
