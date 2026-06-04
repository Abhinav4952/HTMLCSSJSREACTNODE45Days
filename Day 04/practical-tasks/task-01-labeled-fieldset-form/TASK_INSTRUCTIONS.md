# Task 01 — Labeled Controls Inside a Fieldset

## Summary

Build a **conference registration** snippet (not a full backend) with `<fieldset>` + `<legend>` grouping **ticket type** radios and a second fieldset for **contact** fields. Every input must have an associated label.

## Learning goals

- Use `fieldset`/`legend` for related radios.
- Wire `label for` to matching `id` on inputs.

## Provided files

- `index.html`, `styles/main.css`

## Constraints

- `action="#"` and `method="post"` on the outer form unless TODO says otherwise.
- No JavaScript.

## `TODO` map

| TODO | Done means |
|------|------------|
| form | `<form action="#" method="post">` wrapping fields |
| ticket fieldset | ≥2 radios with shared `name` |
| contact fieldset | text + email fields with labels |
| submit | `<button type="submit">Register</button>` |

## Manual checks

- [ ] Clicking each label toggles/focuses the correct control.
