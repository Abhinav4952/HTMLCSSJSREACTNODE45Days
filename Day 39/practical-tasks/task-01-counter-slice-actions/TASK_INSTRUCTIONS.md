# Task 1 — Counter slice actions

## Summary

Implement the **reducers** for a Redux Toolkit **`counter`** slice so **`increment`**, **`decrement`**, and **`reset`** actually update `state.value`. The React UI and store wiring are already provided.

## Learning goals

- Write RTK **slice reducers** with safe “mutative” syntax (Immer).
- Connect **actions** to UI events via **`useDispatch`**.

## Provided files

- `src/app/store.js` — registers `counter` reducer.
- `src/features/counter/counterSlice.js` — **your primary edit surface** (contains `TODO`s).
- `src/components/Counter.jsx` — reads state and dispatches actions (read-only unless instructor says otherwise).
- `src/main.jsx` — mounts `<Provider store={store}>`.

## Prerequisites

- Day 39 theory sections through `createSlice`.

## What you will implement

1. `increment` increases `value` by **1**.
2. `decrement` decreases `value` by **1** but **never below 0**.
3. `reset` sets `value` to **0**.

## Constraints

- Only edit files containing `TODO(Day39-task01)`.
- Do not add Redux Saga, Observable middleware, or extra global state libraries.

## Step-by-step guidance

1. Open `counterSlice.js` and implement the three reducer bodies.
2. Run the dev server and verify each button changes the displayed number.

## How to run and verify

From the repository root:

```bash
cd "Day 39/practical-tasks/task-01-counter-slice-actions"
npm install
npm run dev
```

Optional compile check:

```bash
npm run build
```

### Manual checks

- [ ] `+1` / `-1` / `Reset` behave per requirements.
- [ ] Counter never displays a negative integer.

## `TODO` map

| `counterSlice.js` | Done means |
|-------------------|------------|
| `increment` / `decrement` / `reset` | Match the behavioral contract above. |

## Submission checklist (Git)

- [ ] Only intentional files changed.
- [ ] No `node_modules` committed.

## Hints (optional)

<details>
<summary>Clamp at zero</summary>

Use `Math.max(0, state.value - 1)` or branch on `state.value` before decrementing.

</details>
