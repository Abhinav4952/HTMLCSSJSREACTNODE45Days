# Task 04 — Structured Profile Page

## Summary

Build a small **personal profile** page that demonstrates document structure taught on Day 01: global metadata, a single clear `<h1>`, `<main>` with two `<section>` blocks, and a `<footer>` with a last-updated note.

## Learning goals

- Compose a complete valid HTML5 document without copying Task 01 verbatim.
- Use landmarks (`<header>`, `<main>`, `<footer>`) appropriately.
- Link a single stylesheet and keep paths relative and correct.

## Provided files

- `index.html` — skeleton with TODOs.
- `styles/main.css` — light typography; you may extend within this file only if TODO allows (default: only fill HTML TODOs).

## Prerequisites

- Tasks 01–03 completed or understood.

## What you will implement

1. Replace placeholder text with **your own** bio (two short paragraphs across sections).
2. Complete all `TODO(Day01-task04)` markers in `index.html`.
3. Ensure `<title>` and visible `<h1>` match your chosen page subject.

## Constraints

- No `<iframe>`, no external CDNs, no JavaScript for this task.
- English copy unless instructor approves another language (still set `lang` accordingly).

## How to run and verify

### Manual checks

- [ ] Valid outline: one `<h1>`, each `<section>` has an `<h2>`.
- [ ] `<header>` wraps site/page title area; `<main>` wraps primary bio; `<footer>` has `small` text with a fake or real “Last updated” date.
- [ ] `styles/main.css` linked and applied.

## `TODO` map

| TODO | Done means |
|------|------------|
| title | Descriptive `<title>` |
| stylesheet | Link to `styles/main.css` |
| header content | Your name in heading context |
| section intros | Meaningful `<h2>` titles |
| paragraphs | Original bio text, not lorem ipsum |
| footer date | `Last updated:` line with ISO-like date |

## Submission checklist (Git)

- [ ] Original wording in bio sections

## Hints

<details><summary>Show hints</summary>

Use `<section aria-labelledby="...">` only if you also set matching `id` on headings—optional for this task.

</details>
