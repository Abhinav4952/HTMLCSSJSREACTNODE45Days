# Task 02 — Head Metadata Basics

## Summary

Extend a starter page with **author**, **description**, and **theme color** meta tags plus a `<link rel="icon">` pointing at a provided SVG favicon. You will practice keeping metadata truthful and concise.

## Learning goals

- Choose appropriate values for `name="author"` and `name="description"`.
- Understand `theme-color` as a progressive enhancement for browser chrome.
- Link a favicon without breaking relative paths.

## Provided files

- `index.html` — partial head/body.
- `assets/favicon.svg` — tiny placeholder graphic (do not replace unless asked).

## Prerequisites

- Completed Task 01 concepts (charset, viewport, title).

## What you will implement

1. All `TODO` items in `index.html` resolved.
2. Description meta between **120–180 characters** (inclusive) summarizing this lab page in your own words.

## Constraints

- Do not invent a fake company; describe the **course lab** honestly.
- Do not add tracking scripts.

## Step-by-step guidance

1. Open `index.html` and complete each TODO in order.
2. Count characters for `description` (editors often show column/selection counts).
3. Open the page and confirm the favicon appears in the tab (may require hard refresh).

## How to run and verify

### Install dependencies

None.

### Run tests

Not applicable.

### Manual checks

- [ ] `author` meta contains your name or agreed pseudonym.
- [ ] `description` length within 120–180 characters.
- [ ] Favicon loads (no broken image icon in tab in Chromium-based browsers).

## `TODO` map

| TODO | Done means |
|------|------------|
| `Day01-task02` author | `<meta name="author" content="...">` |
| `Day01-task02` description | Length 120–180 chars, unique wording |
| `Day01-task02` theme-color | Reasonable hex color in `content` |
| `Day01-task02` favicon link | `<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">` or equivalent correct path |

## Submission checklist (Git)

- [ ] Intentional edits only
- [ ] No secrets

## Hints

<details><summary>Show hints</summary>

Use an online character counter if unsure. `theme-color` is optional in some browsers—still include it for practice.

</details>
