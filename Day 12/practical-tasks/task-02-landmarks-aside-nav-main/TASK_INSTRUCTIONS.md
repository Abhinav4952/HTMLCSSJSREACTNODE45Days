# Task 02 — Landmarks: `aside`, `nav`, `main`

## Summary

Convert a starter console layout into a **semantic two-column** structure: primary content in `main`, supporting material in `aside`, and a labeled `nav` in the header.

## Learning goals

- Choose `aside` vs `nav` intentionally.
- Provide `aria-label` when multiple landmarks of the same kind could confuse users.

## Provided files

- `index.html`
- `styles/main.css`

## Prerequisites

- Task 01 + Day 12 theory.

## What you will implement

Complete all `TODO(Day12-task02)` markers:

1. Add header `nav` with `aria-label` and three `#` links.
2. Add a brief HTML comment above `.layout` explaining why `main` appears before `aside` in DOM order.
3. Add original paragraph copy in `main`.
4. Populate `aside` with related links + a `figure` code snippet.

## Constraints

- Keep a single `main` with `id="main"`.
- Do not use `iframe`.

## Step-by-step guidance

1. HTML semantics first.
2. Then enhance `nav` responsiveness in CSS.

## How to run and verify

### Manual checks

- [ ] Accessibility tree shows labeled `nav`, `main`, `aside`.
- [ ] `figure` contains `pre`/`code` and a `figcaption`.

## `TODO` map

| TODO | Done means |
|------|------------|
| Header nav | `aria-label` + 3 links |
| Wrapper semantics | `main`/`aside` structure is explicit in HTML |
| Main paragraph | Original copy |
| Aside content | Related links + figure snippet |
| CSS nav + focus | Readable responsive nav + visible `:focus-visible` |

## Submission checklist (Git)

- [ ] TODOs removed

## Hints

<details><summary>Wrapper replacement</summary>

You may keep `.layout` on a `div` if needed, but `main` and `aside` should be real elements inside it—not another anonymous-only layout.

</details>
