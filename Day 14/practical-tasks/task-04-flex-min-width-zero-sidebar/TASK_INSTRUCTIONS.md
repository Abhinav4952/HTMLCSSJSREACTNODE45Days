# Task 04 — Flex `min-width: 0` Sidebar (Challenge)

## Summary

Fix a classic flex overflow: a **long unbroken string** in a flexible main pane forces horizontal scrolling unless min-size defaults are overridden.

## Learning goals

- Apply `min-width: 0` (or equivalent) where flex items must shrink below content min-content.

## Provided files

- `index.html`, `styles/main.css`

## Prerequisites

- Day 14 theory: `min-width: auto` footgun.

## What you will implement

Complete all `TODO(Day14-task04)` markers.

## Constraints

- Do not delete the long token string (you may wrap CSS around it).

## How to run and verify

### Manual checks

- [ ] At **390px** viewport width: **no** horizontal scrollbar on `body` due to this layout.
- [ ] Token remains readable/wrapped—not clipped invisibly without scroll.

## `TODO` map

| TODO | Done means |
|------|------------|
| CSS | min-size + wrapping fix |
| CSS token | `--shell-bg` used |
| HTML | Explanation paragraph |

## Submission checklist (Git)

- [ ] TODOs removed
