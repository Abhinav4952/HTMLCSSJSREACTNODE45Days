# Task 04 — **Challenge** — Column Drop Without Overflow

## Summary

You have a row of “cards” that should wrap (`flex-wrap`). One card contains an **absurdly long unbroken string** (a URL). The row overflows horizontally unless you apply the **flex min-width** discipline correctly.

## Acceptance

- At 360px viewport width: **no horizontal page scrollbar** attributable to `.row`.
- Cards wrap into multiple rows; each card should be at least comfortable to read (you may adjust padding).

## `TODO` map

| TODO | Done means |
|------|------------|
| `.row` | flex wrap row with gap |
| `.card` | `flex: 1 1 220px` (or similar) + `min-width: 0` |
| `.card code` | wraps long token (`overflow-wrap:anywhere` or `word-break`) |
