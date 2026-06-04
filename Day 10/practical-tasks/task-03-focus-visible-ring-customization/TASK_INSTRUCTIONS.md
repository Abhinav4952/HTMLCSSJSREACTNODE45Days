# Task 03 — **Challenge** — `:focus-visible` Ring on a Dark Panel

## Summary

You have dark buttons on a dark panel. Default focus outlines may be **low contrast** or inconsistent across browsers. Implement a **strong, on-brand** focus treatment using `:focus-visible` (not plain `:focus` only) and ensure **mouse clicks** don’t get an obnoxious ring if the browser heuristics suppress it—but keyboard users always get a visible focus.

## Acceptance

- Keyboard tabbing through buttons shows a clearly visible ring/shadow.
- Styles remain high-contrast on `#0b1220` background.

## Constraints

- Do not remove focus outlines without replacement.
- Avoid `outline: none` unless paired with a demonstrably visible `:focus-visible` alternative.

## `TODO` map

| TODO | Done means |
|------|------------|
| `.panel button:focus-visible` | custom ring |
| hover | optional subtle hover state |
