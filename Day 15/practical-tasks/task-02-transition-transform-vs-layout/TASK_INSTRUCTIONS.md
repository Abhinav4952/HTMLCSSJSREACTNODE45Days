# Task 02 — Transition: Layout vs Transform (Challenge)

## Summary

Build two hover/focus micro-interactions that look similar in intent but differ mechanically: one animates **`width`** (layout), the other animates **`transform`** (typically cheaper).

## Learning goals

- Feel the difference between layout transitions and transform transitions.
- Add a **reduced motion** escape hatch.

## Provided files

- `index.html`, `styles/main.css`

## Prerequisites

- Day 15 theory: transform vs layout + `prefers-reduced-motion`.

## What you will implement

Complete all `TODO(Day15-task02)` markers.

## Constraints

- No JavaScript.

## How to run and verify

### Manual checks

- [ ] Both cards respond on hover **and** keyboard focus (`:focus-visible` already present on cards).
- [ ] Reduced motion mode removes the “big” transitions (verify via DevTools emulation).

## `TODO` map

| TODO | Done means |
|------|------------|
| CSS layout card | Width transition per spec |
| CSS transform card | Transform transition per spec |
| CSS reduced motion | Disables/neutralizes motion |
| HTML lede | Two-sentence reflection |

## Submission checklist (Git)

- [ ] TODOs removed
