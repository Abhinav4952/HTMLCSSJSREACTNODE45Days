# Task 2 — Signup form validation UX

## Summary

Build a **controlled** signup form with **inline validation**, **disabled submit** while invalid, and accessible error text.

## What you will implement

1. Three controlled fields: **full name**, **email**, **password**.
2. Use the provided `validate` helper; derive errors with **`useMemo`** when any field changes.
3. Submit disabled when errors exist.
4. Show per-field `<p className="error" role="alert">` messages.
5. Valid submit: `preventDefault` + `alert('Account request recorded (demo)')` (or similar).

## How to run and verify

```bash
cd "Day 37/practical-tasks/task-02-signup-form-validate"
npm install
npm run dev
```

## Constraints

- Only edit files with `TODO(Day37-task02)`.

## Manual checks

- [ ] Submit starts disabled.
- [ ] Password `1234567` shows length error; length 8 clears that error.
- [ ] Email without `@` shows email error.

## `TODO` map

| `SignupForm.jsx` | Done means |
|------------------|------------|
| All Day37-task02 TODO lines | Controlled fields + memoized errors + disabled submit + alerts. |

## Submission checklist (Git)

- [ ] `npm run build` passes.
