# Task 04 — Inheritance Reading Page

## Summary

Demonstrate **CSS inheritance** by styling `body` and selectively overriding inside an `<aside class="note">`. You will also add a short explanatory paragraph using `<code>` for property names.

## Learning goals

- See which properties inherit (`color`, `font-family`) vs which do not (`background`, `border`) without advanced cascade topics yet.
- Override inherited values with a more specific rule.

## Provided files

- `index.html`, `styles/main.css`

## What you will implement

1. HTML: complete TODOs for article + aside structure and original copy.
2. CSS: set global base on `body`; style `.note` with different `font-family` and `background-color`.

## `TODO` map

| TODO | Done means |
|------|------------|
| HTML structure | `<main>` with `<article>` and `<aside class="note">` |
| article text | ≥120 words original |
| aside text | ≥40 words explaining inheritance in your own words, includes `<code>` mentioning at least two property names |
| CSS body | `color`, `font-family`, `line-height` |
| CSS .note | Different `font-family`, non-transparent `background-color`, `border-left` or `padding` for emphasis |

## Manual checks

- [ ] Aside visually distinct from article while still inheriting `color` unless you intentionally override (either pattern OK if explained in text).
