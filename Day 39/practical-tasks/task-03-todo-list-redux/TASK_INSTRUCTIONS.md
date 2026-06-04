# Task 3 — Todo list reducers

## Summary

Implement **`addTodo`**, **`toggleTodo`**, and **`removeTodo`** reducers for a small todo list stored in Redux.

## Learning goals

- Update **array state** immutably with RTK + Immer ergonomics.
- Treat **`action.payload`** as the input contract from the UI.

## Provided files

- `src/features/todos/todosSlice.js` — **edit surface**.
- `src/components/TodoApp.jsx` — dispatches actions (read-only unless instructor allows).

## What you will implement

1. **`addTodo`**: append `{ id, text, done:false }` using `String(nextId++)` for new ids; ignore empty/whitespace-only payloads.
2. **`toggleTodo`**: flip `done` for the matching `id`.
3. **`removeTodo`**: remove the item with matching `id`.

## Constraints

- Only edit files with `TODO(Day39-task03)`.

## How to run and verify

```bash
cd "Day 39/practical-tasks/task-03-todo-list-redux"
npm install
npm run dev
```

### Manual checks

- [ ] Add creates a new row; empty adds do nothing visible (no blank todos).
- [ ] Checkbox toggles `done` styling (line-through).
- [ ] Remove deletes the correct row only.

## `TODO` map

| `todosSlice.js` | Done means |
|-----------------|------------|
| All Day39-task03 TODO lines | Correct immutable-ish updates for todos. |

## Submission checklist (Git)

- [ ] `npm run build` passes.
