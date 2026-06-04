# Task 01 — **Challenge** — `inline-block` Whitespace Gap

## Summary

The toolbar below uses `display: inline-block` on links. The HTML is formatted “prettily,” which introduces **whitespace text nodes** between items—so you see unwanted gaps.

Fix the gaps using **one** of these allowed strategies (pick one, document it in a CSS comment):

1. **Preferred:** change layout to `display: flex` + `gap` on `.toolbar` (no `inline-block` on items).
2. **Allowed hack:** `font-size: 0` on `.toolbar` and reset font-size on `.toolbar > *`.
3. **Allowed markup hack:** edit `index.html` to remove inter-tag whitespace between items (least preferred).

## Acceptance

- Visual gaps between items are gone at default zoom.
- Toolbar still wraps on narrow screens without horizontal page scroll from the toolbar alone.

## `TODO` map

| TODO | Done means |
|------|------------|
| strategy comment | States which allowed strategy you picked |
| implementation | Meets acceptance |
