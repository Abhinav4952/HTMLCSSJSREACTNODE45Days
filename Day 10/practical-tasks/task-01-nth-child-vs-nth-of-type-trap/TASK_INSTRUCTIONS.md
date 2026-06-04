# Task 01 — **Challenge** — `:nth-child` vs `:nth-of-type` Table Stripes

## Summary

A well-meaning stripe rule colors the **wrong rows** because it uses `:nth-child` at the wrong scope. Fix striping so:

- **Header row(s)** in `<thead>` keep a distinct background.
- **Only `<tbody>` data rows** zebra stripe (even/odd alternating), never the header.

You may edit **only** `styles/main.css` unless you convince your instructor otherwise.

## Acceptance

- Visual: header looks like a header; body rows alternate.
- No horizontal scroll introduced.

## `TODO` map

| TODO | Done means |
|------|------------|
| fix selectors | Correct zebra in tbody only |
