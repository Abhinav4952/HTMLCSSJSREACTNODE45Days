# Task 04 — **Challenge** — Stacking Context `z-index` Mystery

## Summary

Three overlays exist: a scrim, a modal card, and a toast. They render in the wrong order despite “large” `z-index` numbers on the toast. Fix stacking using **`isolation`** and/or **minimal `z-index` adjustments** on the correct ancestors—**without** setting absurd values like `999999`.

## Rules

- Do not edit `index.html`.
- Avoid `z-index` values above **60** (inclusive).
- Prefer `isolation: isolate` where it clarifies layering.

## Acceptance

- Toast appears **above** modal.
- Modal appears **above** scrim.
- Clicking the toast button remains possible (no invisible overlay blocking hits).

## `TODO` map

| TODO | Done means |
|------|------------|
| fix stacking | Meets acceptance |
