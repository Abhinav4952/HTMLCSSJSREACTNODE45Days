# Task 03 — External Assets, `defer`, and `async`

## Summary

You will wire `styles/main.css` and three small scripts to observe **parse order** and **`defer`** behavior. One script is intentionally written to log order; you must fix loading attributes so the log matches the acceptance criteria.

## Learning goals

- Link an external stylesheet from a subfolder.
- Load your own module script with `defer` (or place it correctly) so it runs after the DOM exists.
- Choose `async` only for an independent helper that does not rely on DOM order beyond `document.body` existing.

## Provided files

- `index.html`
- `styles/main.css`
- `scripts/log-inline.js`, `scripts/app-deferred.js`, `scripts/helper-async.js`

## Prerequisites

- Read the theory section on `<script>` loading strategies.

## What you will implement

1. Link `styles/main.css` from `index.html` (TODO).
2. Add `<script>` tags for the three files per TODO instructions so that when you open the browser console you see the **log sequence**: `inline` → `helper-async may run anytime` (may interleave) → `deferred app sees: ...` where the deferred app prints the greeting element text **without** null errors.

## Constraints

- Do not inline the CSS/JS contents for this task—use external files as provided.
- Do not rename provided JS files.

## Step-by-step guidance

1. Complete the `<link>` TODO.
2. Add `log-inline.js` without `defer`/`async` in the `<head>` exactly where the TODO says (simulates legacy inline-order logging).
3. Add `helper-async.js` with `async` as indicated.
4. Add `app-deferred.js` with `defer` and ensure it appears **before** `</body>` or in `<head>` with `defer`—pick one approach and verify console output.

## How to run and verify

### Install dependencies

None.

### Manual checks

- [ ] Page is styled (body has max-width and font from CSS).
- [ ] Console shows `deferred app sees: Hello from Day 01 task 03` (exact substring) after refresh.
- [ ] No uncaught `TypeError` about null/undefined.

## `TODO` map

| TODO | Done means |
|------|------------|
| stylesheet link | `<link rel="stylesheet" href="styles/main.css">` in head |
| inline logger | `log-inline.js` included as blocking script in head per comment |
| async helper | `helper-async.js` with `async` attribute |
| deferred app | `app-deferred.js` with `defer` and correct `src` |

## Submission checklist (Git)

- [ ] Console evidence noted in commit message or instructor form if required

## Hints

<details><summary>Show hints</summary>

If you see `null` from the deferred script, it ran before the `#greeting` node existed—use `defer` and keep the element in HTML before the deferred script’s execution point, or move the script to end of body **with** `defer` in head per best practice.

</details>
