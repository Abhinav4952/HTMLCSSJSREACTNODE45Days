# Task 03 — Opacity Stacking Clinic

## Summary

You will build two visually related overlays on a striped background: one using **`opacity`** (creates a transparency *group*) and one using **`rgba()`/`hsla()` alpha** on a background layer. The goal is to *feel* the Day 11 theory difference in your eyes and DevTools, not to pixel-match a screenshot.

## Learning goals

- Predict how `opacity` on a container affects text vs backgrounds.
- Choose alpha colors when you want readable text over busy imagery.

## Provided files

- `index.html`
- `styles/main.css`

## Prerequisites

- Day 11 theory: `opacity` vs alpha colors.

## What you will implement

1. Complete all `TODO(Day11-task03)` markers in HTML and CSS.
2. **Stack A** must use `opacity` in a way that **fades the paragraph text** relative to normal body text (not merely the background).
3. **Stack B** must keep paragraph text **strong** (near-normal foreground) while still showing a translucent tinted layer above the stripes (via alpha background, not by fading the whole subtree with `opacity`).
4. Add the checklist `<code>` prediction about nested opacity multiplication (one sentence is enough).

## Constraints

- Do not change the HTML tag hierarchy (no extra wrapper elements). Work with `.stack`, `.stack__media`, `.stack__content`.
- Do not use `!important`.

## Step-by-step guidance

1. Style Stack A first: verify paragraph color/opacity in DevTools computed styles.
2. Style Stack B: verify paragraph text is not stuck inside an `opacity` group that dims it.
3. Complete checklist note.

## How to run and verify

### Manual checks

- [ ] Stack A paragraph visibly more faded than Stack B paragraph (side-by-side).
- [ ] Stack B still shows stripes through a tinted overlay.
- [ ] Checklist item contains a `<code>` snippet/note about opacity multiplication / grouping.

## `TODO` map

| TODO | Done means |
|------|------------|
| HTML paragraphs | Two distinct student-written sentences per instructions |
| HTML checklist | Includes `<code>`…`</code>` with opacity math/prediction |
| CSS Stack A | Uses `opacity` consistent with requirements |
| CSS Stack B | Uses alpha background layering; text remains strong |

## Submission checklist (Git)

- [ ] No secrets; only intentional files changed

## Hints

<details><summary>If text won’t fade in Stack A</summary>

`opacity` on `.stack` affects everything inside—including text. If you only tint `::before` without grouping, you might accidentally recreate Stack B’s behavior.

</details>
