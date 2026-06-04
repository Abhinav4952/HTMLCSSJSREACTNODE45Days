# Task 04 — Product Card Gallery

## Summary

Combine selector practice and decoration: build a **gallery** of four `<article class="card">` elements representing fictional “modules” of a course app. Use **at least one** child combinator rule and **one** adjacent sibling rule in your CSS beyond simple classes.

## Learning goals

- Integrate layout + typography + borders from Tasks 01–03.
- Keep keyboard focus visible on links/buttons inside cards.

## Provided files

- `index.html`, `styles/main.css`

## Constraints

- No JavaScript.
- No external CSS frameworks.

## `TODO` map

| TODO | Done means |
|------|------------|
| HTML | Four cards with title, 1–2 sentence description, and `<a class="cta" href="#">Open</a>` |
| CSS gallery | responsive grid or flex that fits ≥2 columns on wide screens and 1 column on narrow |
| CSS combinator | document in CSS comment which rule uses `>` and which uses `+` |
| CSS price/badge | include `.meta` line with `.badge` + `.price`; style `.meta > .badge` and `.badge + .price` meaningfully |

## Manual checks

- [ ] All CTAs keyboard-focusable with visible `:focus-visible`.
