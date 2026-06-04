import { createSlice } from '@reduxjs/toolkit'

let nextId = 3

const todosSlice = createSlice({
  name: 'todos',
  initialState: {
    items: [
      { id: 'seed-1', text: 'Learn slice reducers', done: true },
      { id: 'seed-2', text: 'Wire React components', done: false },
    ],
  },
  reducers: {
    addTodo: (state, action) => {
      // TODO(Day39-task03): Append a new item `{ id, text, done:false }`.
      // Use `String(nextId++)` for ids. Ignore empty/whitespace-only `action.payload`.
    },
    toggleTodo: (state, action) => {
      // TODO(Day39-task03): Flip `done` for the item whose `id` matches `action.payload`.
    },
    removeTodo: (state, action) => {
      // TODO(Day39-task03): Remove the item whose `id` matches `action.payload`.
    },
  },
})

export const { addTodo, removeTodo, toggleTodo } = todosSlice.actions
export default todosSlice.reducer
