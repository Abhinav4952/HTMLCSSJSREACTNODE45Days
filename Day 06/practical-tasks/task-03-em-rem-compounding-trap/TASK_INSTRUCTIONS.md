# Task 03 — **Challenge** — `em` Compounding & the “Chip Explosion”

## Summary

You inherit a “design system” that **looks fine at one nesting depth** but becomes comically wrong inside nested `.module` containers: chips grow/shrink unpredictably, and vertical rhythm falls apart. Your job is to **fix the CSS only** (do not change `index.html` structure) so that:

- nested modules **do not change** the computed `font-size` of unrelated descendants (hint: stop chaining `em` on `font-size` for wrappers),
- chip padding and radius remain visually stable across nesting levels,
- the page still expresses hierarchy using **rem-based** type scale variables.

This task is intentionally **mean**: it simulates a real refactor where `em` looked elegant until the third wrapper.

## Learning goals

- Predict **compounding** with nested `font-size: …em`.
- Choose **`rem`** for “global” spacing and component padding when nesting is unknown.
- Use **`em` only where local scaling is truly desired** (or avoid entirely here).

## Provided files

- `index.html` (read-only for this task)
- `styles/main.css` (contains the footgun + TODOs)

## Prerequisites

- Day 06 theory sections on `rem` vs `em`.

## What you will implement

1. Meet the **acceptance checklist** below by editing **only** `styles/main.css`.
2. Remove or resolve every `/* TODO(Day06-task03): ... */` comment as you complete work (replace with final rules).

## Constraints

- **Forbidden:** editing `index.html` (no cheating by flattening DOM), unless instructor explicitly overrides.
- Avoid `!important`.

## Acceptance checklist (manual)

- [ ] At **nesting depth 3**, `.chip` text is within **±10%** of the visual size of depth-1 `.chip` text (use DevTools computed font-size; they should be nearly equal).
- [ ] `.chip` vertical padding does not balloon at depth 3 (computed top+bottom padding within **±6px** of depth-1 chip padding).
- [ ] `h2` hierarchy still reads larger than body text at all depths (you may adjust rem scale).

## `TODO` map

| TODO | Done means |
|------|------------|
| module font-size footgun | Remove compounding `font-size` behavior on `.module .module` chain OR reset strategy that prevents runaway scaling |
| chip padding | Convert chip padding/border-radius to stable units |
| type scale | Provide `--step-*` rem variables and apply to headings/body without em-compounding surprises |

## Hints

<details><summary>Big hint (use only if stuck)</summary>

The footgun is `font-size: 0.95em` on nested `.module`. Switch module “shrink” to **padding** changes in `rem`, or remove nested font-size entirely and use border/background depth instead.

</details>
