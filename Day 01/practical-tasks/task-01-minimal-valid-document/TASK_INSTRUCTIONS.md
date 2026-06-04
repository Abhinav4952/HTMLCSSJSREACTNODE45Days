# Task 01 — Minimal Valid HTML5 Document

## Summary

You will complete a bare-bones HTML5 page that validates the ideas from Day 01 theory: correct doctype, `lang` on `<html>`, a responsible `<head>`, and visible content in `<body>`.

## Learning goals

- Place `<!DOCTYPE html>` as the first statement in the file.
- Add `lang` on `<html>` appropriate to your page (use `en` unless your instructor directs otherwise).
- Include `charset` and `viewport` meta tags and a meaningful `<title>`.

## Provided files

- `index.html` — starter shell with `TODO` comments marking missing pieces.

## Prerequisites

- Read `DAY-01-THEORY-AND-REFERENCE.md` sections on doctype and `<head>`.

## What you will implement

1. A standards-mode HTML5 document that opens without console errors related to your edits.
2. All items listed in the [TODO map](#todo-map) completed (remove the `TODO` comments as you go or leave resolved notes per instructor preference—default: replace with final markup, no stale TODOs).

## Constraints

- Do not add frameworks or build tools.
- Keep the page accessible: include `alt` text if you add any `<img>` (optional for this task).

## Step-by-step guidance

1. Open `index.html` in your editor and locate each `<!-- TODO(Day01-task01): ... -->` comment.
2. Fill in doctype, attributes, meta tags, and body content per the TODO text.
3. Open the file in a browser and verify the tab title updates.

## How to run and verify

### Install dependencies

None for this task.

### Run tests (JavaScript / Node logic tasks)

Not applicable.

### Run the app (React / Node server tasks)

Not applicable.

### Manual checks (all tasks)

- [ ] View source shows `<!DOCTYPE html>` on line 1.
- [ ] `<html>` has a `lang` attribute.
- [ ] `<meta charset="utf-8">` appears in `<head>`.
- [ ] `<meta name="viewport" ...>` is present.
- [ ] `<title>` is unique and human-readable (not “Document”).

## `TODO` map

| Location | Done means |
|----------|------------|
| `index.html` — doctype | `<!DOCTYPE html>` present at top |
| `index.html` — `<html>` | `lang` attribute set |
| `index.html` — charset | UTF-8 meta present |
| `index.html` — viewport | Mobile-friendly viewport meta present |
| `index.html` — title | Descriptive `<title>` |
| `index.html` — body | Replace placeholder with a short greeting paragraph |

## Submission checklist (Git)

- [ ] Only intentional files changed
- [ ] No secrets committed
- [ ] Page loads locally from disk or via `npx serve .`

## Hints (optional collapsible section)

<details><summary>Show hints</summary>

- The doctype has no closing tag.
- Copy the viewport string exactly from the theory file to avoid typos.

</details>
