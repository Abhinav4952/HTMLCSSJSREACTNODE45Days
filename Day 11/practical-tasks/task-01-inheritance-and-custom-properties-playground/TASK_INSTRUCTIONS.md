# Task 01 — Inheritance &amp; Custom Properties Playground

## Summary

You will wire **custom properties** on `body` and two labeled regions so nested cards **inherit** typography color through `var()` while keeping **non-inherited** properties (like `background-color`) explicit and predictable.

## Learning goals

- Explain the difference between inherited `color` and explicit `background-color` on nested components.
- Use `--tokens` to avoid duplicating hex values across a small layout.

## Provided files

- `index.html` — two regions + nested card markup
- `styles/main.css` — starter layout; your cascade work lives here

## Prerequisites

- Read Day 11 theory sections on inheritance and custom properties.

## What you will implement

1. Complete every `TODO(Day11-task01)` marker in **HTML** and **CSS**.
2. `:root` (or `body`) defines default `--region-fg` and `--region-accent`.
3. `[data-region="marketing"]` and `[data-region="ops"]` each override both variables with **different** colors.
4. Panels use `color: var(--region-fg)` so nested paragraphs inherit region text color without per-element `color` rules.
5. Cards show a left accent bar using `border-left` + `var(--region-accent)`.
6. Cards have a subtle tinted background derived from `--region-accent` **without** applying `opacity` to the entire card.

## Constraints

- Do not use `!important`.
- Do not set `opacity` on `.card` or `.panel` for this task (use alpha in colors instead).

## Step-by-step guidance

1. Open `index.html` in a browser with DevTools.
2. Implement CSS variables and region overrides.
3. Replace placeholder copy in HTML TODOs with short original sentences.
4. In DevTools → Computed, click `color` on a nested `<p>` and confirm inheritance chain.

## How to run and verify

### Manual checks (all tasks)

- [ ] Marketing and Ops regions are visibly different in **text** and **accent bar** colors.
- [ ] Nested `<p>` inside `.card` inherits region text color (no extra `p { color: … }` needed).
- [ ] Card background tint is present and text remains readable (contrast sanity check).
- [ ] HTML copy TODOs are completed with your own wording.

## `TODO` map

| Location | Done means |
|----------|------------|
| HTML TODOs | Original cohort-specific copy + explanatory sentence in Ops |
| CSS TODO chain | Tokens on `:root`, overrides per `data-region`, `color` via `var`, card accent + tinted background |

## Submission checklist (Git)

- [ ] Only intentional files changed
- [ ] No secrets committed

## Hints

<details><summary>color-mix availability</summary>

If your browser is older, prefer `rgba()`/`hsl()` with fixed alpha rather than `color-mix()`.

</details>
