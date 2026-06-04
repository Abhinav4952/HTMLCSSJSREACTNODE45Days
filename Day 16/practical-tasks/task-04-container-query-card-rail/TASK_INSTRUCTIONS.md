# Task 04 — Container Query Card Rail (Challenge)

## Summary

Use **`@container`** so `.card` layout responds to the **rail** width, demonstrating why container queries beat “one breakpoint for the whole page.”

## Learning goals

- Create a named inline-size container and write `@container` rules against it.

## Provided files

- `index.html`, `styles/main.css`

## Prerequisites

- Day 16 theory: container queries.

## What you will implement

Complete all `TODO(Day16-task04)` markers.

## Constraints

- Do not duplicate cards in HTML between rails (markup is intentionally identical).
- Prefer container queries for the card mini-layout; any viewport fallback must be justified in the HTML note.

## How to run and verify

### Manual checks

- [ ] Narrow rail: cards remain stacked.
- [ ] Wide rail: cards switch to the specified two-column mini-layout at your container threshold.

## `TODO` map

| TODO | Done means |
|------|------------|
| CSS container | `container-type` + `container-name` on `.rail__body` |
| CSS @container | Card layout changes at rail width |
| HTML note | Documents threshold + testing/fallback |

## Submission checklist (Git)

- [ ] TODOs removed
