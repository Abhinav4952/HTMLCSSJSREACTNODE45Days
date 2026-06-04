# Task 02 — Specificity Duel Scoreboard (Challenge)

## Summary

Three “matches” print conflicting color declarations. You may only adjust **CSS** (plus the allowed HTML text TODO) so each champion line ends on the exact hex color specified—**without** `!important` and **without** inline styles.

## Learning goals

- Read DevTools “Rules” panel like a scoreboard: see which declaration loses and why.
- Engineer a winning selector that is **specific enough**, not merely “long.”

## Provided files

- `index.html` — match structure (do not change tags/classes except subtitle copy TODO)
- `styles/main.css` — conflicting candidates + your winning moves

## Prerequisites

- Day 11 theory: specificity tuple model.

## What you will implement

1. **Match 1:** Add **exactly one** new CSS rule so the Match 1 champion line computes to `#7c3aed`.
2. **Match 2:** Add **at most two** new CSS rules targeting Match 2 only so the champion line computes to `#0ea5e9`.
3. **Match 3 (trap):** Beat `#scoreboard .trap { color: … }` using normal specificity mechanics so the trap line computes to `#f97316`.
4. Replace the subtitle HTML `TODO(Day11-task02)` with a one-line explanation in your own words.

## Constraints

- No `!important`.
- No inline `style=""` attributes.
- Do not change HTML structure (no extra wrappers) except completing the subtitle text TODO.

## Step-by-step guidance

1. Open DevTools → select a champion `<p>` → Colors panel → verify computed hex.
2. For each match, start from the current winner and count **IDs / classes / types**.
3. Add the smallest winning selector you can justify.

## How to run and verify

### Manual checks

- [ ] Match 1 computed text color is `#7c3aed`.
- [ ] Match 2 computed text color is `#0ea5e9`.
- [ ] Match 3 computed text color is `#f97316`.
- [ ] You added **≤1** new rule for Match 1, **≤2** new rules for Match 2 (existing noise rules may remain).

## `TODO` map

| TODO | Done means |
|------|------------|
| `styles/main.css` Match 1 | Exactly one added rule; correct winner color |
| `styles/main.css` Match 2 | ≤ two added rules; correct winner color |
| `styles/main.css` Match 3 | Trap beaten without `!important` |
| `index.html` subtitle | Student-written explanation |

## Submission checklist (Git)

- [ ] No devtools-only edits; files saved in repo

## Hints

<details><summary>Trap match hint</summary>

`#scoreboard .trap` is `(1,1,1)` in a simplified ID/class/type mental model. To win, you need a strictly higher tuple **or** tie-break via source order with **equal** specificity (prefer increasing specificity to avoid accidental ties).

</details>
