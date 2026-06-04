# Task 02 — **Challenge** — Margin Collapse Detective

## Summary

A “junior dev” checked in CSS that **looks reasonable** but produces the wrong vertical rhythm between sections. Your job is to **reach an exact target** vertical distance (measured from border-edge to border-edge of key blocks) using **only** `styles/main.css` (HTML is read-only).

Targets (desktop, default zoom):

- Between `#a` bottom border and `#b` top border: **exactly 32px** gap (not 40px, not 24px).
- Between `#b` bottom border and `#c` top border: **exactly 24px** gap.

You may not edit `index.html`.

## Learning goals

- Identify sibling margin collapse vs other spacing mechanisms.
- Choose the smallest fix that meets measurement targets (not “throw flex at it”).

## Provided files

- `index.html` (read-only)
- `styles/main.css`

## Acceptance

Use DevTools ruler/measurement (Firefox measuring tool or computed positions) to verify targets within **±1px**.

## `TODO` map

| TODO | Done means |
|------|------------|
| diagnosis comment | Top of CSS file: 4–10 lines explaining which margins collapsed and why |
| fix A–B | Achieve 32px gap with minimal disruption |
| fix B–C | Achieve 24px gap |

## Hints

<details><summary>Spoiler-free hint</summary>

If two margins touch, they may collapse to `max(a,b)`. You can prevent collapse by inserting a **non-collapsing separation** without changing HTML—sometimes padding on a wrapper already exists; sometimes you need `display: flow-root` on the right ancestor already in the HTML tree.

</details>
