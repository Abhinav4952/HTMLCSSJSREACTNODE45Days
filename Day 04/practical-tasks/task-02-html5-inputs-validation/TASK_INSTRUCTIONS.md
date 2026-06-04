# Task 02 — HTML5 Inputs and Validation Attributes

## Summary

Create a **profile editor** form demonstrating `type="url"`, `type="tel"`, `type="number"` with bounds, and `pattern` on a username field with visible help text explaining the pattern.

## Learning goals

- Use validation attributes responsibly with human-readable instructions.

## Provided files

- `index.html`, `styles/main.css`

## Constraints

- Do not collect real secrets; `password` fields are **not** required here.

## `TODO` map

| TODO | Done means |
|------|------------|
| url | Labeled `homepage` url input |
| tel | Labeled `phone` tel input |
| number | Labeled `age` with min 18 max 120 |
| pattern | Labeled `username` with pattern `^[a-z0-9_]{3,15}$` plus `<p class="hint">` explaining allowed characters |

## Manual checks

- [ ] Try submitting empty—browser validation should block with native messages.
