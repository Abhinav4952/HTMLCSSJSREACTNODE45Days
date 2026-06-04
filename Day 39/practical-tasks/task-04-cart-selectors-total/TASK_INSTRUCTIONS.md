# Task 4 — Memoized cart total selector

## Summary

Use **`createSelector`** (re-exported from **`@reduxjs/toolkit`**) to compute a **total checkout price** in cents from seeded cart lines.

## Learning goals

- Write a derived **`selectCartTotalCents`** selector.
- Keep presentation components reading **view data** via selectors.

## Provided files

- `src/features/cart/cartSelectors.js` — **edit surface** (`TODO(Day39-task04)`).
- `src/features/cart/cartSlice.js` — seeded lines (read-only for this task).
- `src/components/CartView.jsx` — displays formatted money.

## What you will implement

1. `selectCartTotalCents` returns \(\sum_i \text{unitPriceCents}_i \times \text{qty}_i\).

## Constraints

- Only edit files with `TODO(Day39-task04)`.

## How to run and verify

```bash
cd "Day 39/practical-tasks/task-04-cart-selectors-total"
npm install
npm run dev
```

### Manual checks

- [ ] Total matches **$18.97** for the seeded data (`499×2 + 899×1` cents).

## `TODO` map

| `cartSelectors.js` | Done means |
|--------------------|------------|
| `selectCartTotalCents` | Correct sum; uses `createSelector`. |

## Submission checklist (Git)

- [ ] `npm run build` passes.
