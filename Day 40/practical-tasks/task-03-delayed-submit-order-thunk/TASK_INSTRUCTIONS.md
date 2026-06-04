# Task 3 — Mocked checkout submit (`createAsyncThunk`)

## Summary

Implement **`extraReducers`** for a **`submitOrder`** thunk that **waits ~500ms** then returns a **confirmation id**, or rejects when the cart lines array is empty (not used by the starter UI, but required by the thunk).

## Learning goals

- Model **async mutations** (submit) with explicit status fields.
- Keep synchronous **`resetCheckout`** reducer working alongside thunks.

## Provided files

- `src/features/orders/orderSlice.js` — **edit surface** (`TODO(Day40-task03)`).
- `src/components/CheckoutPanel.jsx` — dispatches `submitOrder` / `resetCheckout` (read-only unless instructor allows).

## Constraints

- Only edit files with `TODO(Day40-task03)`.

## How to run and verify

```bash
cd "Day 40/practical-tasks/task-03-delayed-submit-order-thunk"
npm install
npm run dev
```

### Manual checks

- [ ] Click **Submit demo order** → short delay → **Confirmation:** shows a `DEMO-…` id.
- [ ] **Reset** clears the confirmation and error state.

## `TODO` map

| `orderSlice.js` | Done means |
|-----------------|------------|
| `extraReducers` | Pending/fulfilled/rejected update `status`, `error`, and `lastConfirmationId` appropriately. |

## Submission checklist (Git)

- [ ] `npm run build` passes.
