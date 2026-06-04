# Task 4 — HOC: decorate a `title` prop

## Summary

Implement a tiny **higher-order component** that wraps `SectionCard` to visually **bracket** string titles: `«Title»`.

## What you will implement

1. `withBracketedTitle` in `src/hoc/withBracketedTitle.jsx` per the TODO contract.
2. Do not edit `App.jsx` wiring (`BracketedSection` should start working once the HOC is correct).

## How to run and verify

```bash
cd "Day 38/practical-tasks/task-04-with-prefix-title-hoc"
npm install
npm run dev
```

## Constraints

- Only edit files with `TODO(Day38-task04)` (the HOC file).

## Manual checks

- [ ] Page heading inside the card shows **«Announcements»** (including guillemets characters used in TODO).

## `TODO` map

| `hoc/withBracketedTitle.jsx` | Done means |
|------------------------------|------------|
| Day38-task04 TODO | HOC returns wrapper that transforms `title` strings. |

## Submission checklist (Git)

- [ ] `npm run build` passes.
