# Task 1 — Counter with `useState`

## Summary

Implement a classic **counter** using **`useState`**. Buttons mutate the count through React state (not the DOM directly).

## Learning goals

- Initialize and update numeric state.
- Use **`type="button"`** to avoid accidental form submission in later tasks.

## Provided files

- `src/components/Counter.jsx` — edit surface.

## Prerequisites

- Day 35 theory: `useState` section.

## What you will implement

1. Count starts at **0** and displays in `<output>`.
2. **+1**, **-1**, and **Reset** buttons work.
3. Reset returns count to **0**.

## Constraints

- Only edit files containing `TODO(Day35-task01)`.

## How to run and verify

```bash
cd "Day 35/practical-tasks/task-01-hooks-counter-usestate"
npm install
npm run dev
```

Optional:

```bash
npm run build
```

### Manual checks

- [ ] Clicking +1 / -1 updates the large number.
- [ ] Reset always returns to 0 from arbitrary counts.

## `TODO` map

| File | Done means |
|------|------------|
| `Counter.jsx` | `useState` + wired handlers + live output text. |

## Submission checklist (Git)

- [ ] No `node_modules` committed.
