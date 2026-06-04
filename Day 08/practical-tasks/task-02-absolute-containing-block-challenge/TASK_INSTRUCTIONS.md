# Task 02 — **Challenge** — Absolute Positioning & Containing Blocks

## Summary

A badge is “escaping” to the wrong corner because the **nearest positioned ancestor** is not the card. Fix it **without editing HTML**—only `styles/main.css`.

## Acceptance

- The `.badge` must align to the **top-right inside `.card` inner padding** (10px from the card’s padding edge), not the page edge.
- Must not change HTML.

## `TODO` map

| TODO | Done means |
|------|------------|
| fix | Correct `position`/ancestor strategy so badge anchors to `.card` |

## Hint

<details><summary>Minimal hint</summary>

Which ancestor currently establishes the containing block for `position: absolute`?

</details>
