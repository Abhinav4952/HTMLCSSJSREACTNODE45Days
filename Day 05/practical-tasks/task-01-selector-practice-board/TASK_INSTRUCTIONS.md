# Task 01 — Selector Practice Board

## Summary

Style the provided **swatch board** using only **external CSS** (`styles/main.css`). You must practice type, class, id, descendant, child (`>`), and adjacent sibling (`+`) selectors without changing HTML beyond removing TODO comments (HTML structure is fixed except completing TODO text content if any).

## Learning goals

- Match selectors to DOM shape without over-qualifying.

## Provided files

- `index.html` (read-only structure except TODO text replacements noted)
- `styles/main.css`

## Constraints

- **Do not** change class names or element order in `index.html` unless a TODO explicitly allows it (default: **CSS only** after optional TODO text).
- No `!important`.

## What you will implement

Complete all `TODO(Day05-task01)` rules in `styles/main.css`.

## `TODO` map

| TODO | Done means |
|------|------------|
| type | All `li` in `#board` get list-style none (prepare grid look) |
| class | `.chip` rounded pill background |
| id | `#board` max-width + margin auto |
| descendant | `.row .chip` font-weight 600 |
| child | `.row > .chip:first-child` different border color |
| adjacent | `.row .chip + .chip` margin-left gap using margin |

## Manual checks

- [ ] Two rows look like horizontal chip rows with distinct first chip border.
