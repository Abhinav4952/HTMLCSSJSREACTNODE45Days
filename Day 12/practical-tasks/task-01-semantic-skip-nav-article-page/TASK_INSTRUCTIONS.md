# Task 01 — Semantic Skip Link + Article Page

## Summary

Build a small **newsroom-style** page using HTML5 landmarks: skip navigation, primary `nav`, unique `main`, a tangential `aside`, and a `footer`. Finish with readable CSS including an accessible skip-link pattern.

## Learning goals

- Place `main` correctly and keep the heading outline coherent.
- Implement a skip link that is usable with keyboard only.

## Provided files

- `index.html` — start from placeholder; replace with your semantic structure
- `styles/main.css`

## Prerequisites

- Day 12 theory: sectioning + accessible forms intro.

## What you will implement

1. Remove the placeholder paragraph once your layout exists.
2. Complete all `TODO(Day12-task01)` markers in HTML and CSS.
3. Page contains: skip link, `header` with site title, `nav` with at least 3 links, `main` with `id="main"` containing an `article` with title + two paragraphs, `aside` with related links list, `footer` with small print.
4. Skip link is first in tab order and becomes visible on `:focus`.

## Constraints

- Exactly **one** `main` element.
- No ARIA roles that duplicate default element semantics unless you document why in an HTML comment.

## Step-by-step guidance

1. Sketch landmarks on paper before coding.
2. Implement HTML first; verify headings in DevTools accessibility tree.
3. Add skip-link CSS.

## How to run and verify

### Manual checks

- [ ] Tab from URL bar: first focusable is skip link; activating it moves focus to `#main`.
- [ ] Landmarks exist and read sensibly in accessibility inspector.
- [ ] No placeholder paragraph remains.

## `TODO` map

| TODO | Done means |
|------|------------|
| HTML skip + landmarks | Complete semantic scaffold per requirements |
| CSS skip-link | Hidden-offscreen until focus; visible high-contrast focus styles |
| CSS layout | Simple readable layout for regions |

## Submission checklist (Git)

- [ ] Only intentional files changed

## Hints

<details><summary>Skip link CSS pattern</summary>

Common approach: absolutely positioned offscreen, then `top/left` reset on `:focus` with high `z-index`.

</details>
