# Task 01 — Breakpoint Strategy Worksheet

## Summary

Document a **three-tier breakpoint plan** in HTML, then implement a small **three-band demo** whose layout changes match the plan—using **mobile-first** `min-width` queries only.

## Learning goals

- Tie breakpoints to **layout changes you can name**, not device brands.

## Provided files

- `index.html`, `styles/main.css`

## Prerequisites

- Day 16 theory: breakpoint strategy.

## What you will implement

Complete all `TODO(Day16-task01)` markers:

1. Fill the table cells with real breakpoint names, widths, and behavior bullets.
2. Implement CSS so `.demo` responds at the breakpoints you documented.
3. Write the footnote paragraph explaining the **mid** breakpoint choice.

## Constraints

- Use **`@media (min-width: …)` only** (no `max-width` queries in your submitted CSS).

## Step-by-step guidance

1. Decide your two non-default breakpoints (`rem` recommended).
2. Implement the smallest layout first; add queries incrementally.

## How to run and verify

### Manual checks

- [ ] Table matches CSS (same threshold values within reasonable rounding).
- [ ] No horizontal scroll from `.demo` between 360px and 1200px for typical desktop browsers.

## `TODO` map

| TODO | Done means |
|------|------------|
| Table cells | Completed plan |
| CSS demo | Matches plan; mobile-first |
| CSS tokens | `:root` custom props used |
| Footnote | Explains mid breakpoint |

## Submission checklist (Git)

- [ ] TODOs removed
