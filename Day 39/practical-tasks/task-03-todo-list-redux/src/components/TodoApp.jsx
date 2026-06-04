import { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { addTodo, removeTodo, toggleTodo } from '../features/todos/todosSlice.js'

export default function TodoApp() {
  const items = useSelector((state) => state.todos.items)
  const dispatch = useDispatch()
  const [draft, setDraft] = useState('')

  return (
    <section>
      <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem' }}>
        <input
          type="text"
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          placeholder="New todo text"
          aria-label="New todo text"
        />
        <button
          type="button"
          onClick={() => {
            dispatch(addTodo(draft))
            setDraft('')
          }}
        >
          Add
        </button>
      </div>
      <ul>
        {items.map((todo) => (
          <li key={todo.id} style={{ margin: '0.35rem 0' }}>
            <label style={{ display: 'inline-flex', gap: '0.5rem', alignItems: 'center' }}>
              <input type="checkbox" checked={todo.done} onChange={() => dispatch(toggleTodo(todo.id))} />
              <span style={{ textDecoration: todo.done ? 'line-through' : 'none' }}>{todo.text}</span>
            </label>
            <button type="button" style={{ marginLeft: '0.75rem' }} onClick={() => dispatch(removeTodo(todo.id))}>
              Remove
            </button>
          </li>
        ))}
      </ul>
    </section>
  )
}
