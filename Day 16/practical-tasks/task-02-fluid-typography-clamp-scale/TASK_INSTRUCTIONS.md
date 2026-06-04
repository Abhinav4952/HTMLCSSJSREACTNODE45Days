# Task 02 — Fluid Typography `clamp()` Scale (Challenge)

## Summary

Implement a **fluid typographic ramp** for a long-form article: headings and body copy should scale smoothly across viewports while staying within **bounded min/max** sizes.

## Learning goals

- Use `clamp()` with a `vw`-based preferred value responsibly.
- Pair fluid `font-size` with **line-height** and **measure** (`ch`) constraints.

## Provided files

- `index.html`, `styles/main.css`

## Prerequisites

- Day 16 theory: responsive typography.

## What you will implement

Complete all `TODO(Day16-task02)` markers in HTML and CSS per CSS comment requirements.

## Constraints

- No JavaScript.
- Body paragraph computed `font-size` must be **≥ 16px** at all widths (verify in DevTools).

## How to run and verify

### Manual checks

- [ ] Resize 320px → 1280px: type scales smoothly (no “stair steps”).
- [ ] `h1` computed size never exceeds **3.25rem**.
- [ ] Paragraph measure is capped with `ch` as specified.

## `TODO` map

| TODO | Done means |
|------|------------|
| HTML copy | Original deck + two long paragraphs include required keywords |
| CSS clamp ramp | h1/h2/p each use clamp with vw-based preferred |
| CSS rhythm | Distinct line-heights |
| CSS measure | Paragraph max-width in `ch` |

## Submission checklist (Git)

- [ ] TODOs removed
