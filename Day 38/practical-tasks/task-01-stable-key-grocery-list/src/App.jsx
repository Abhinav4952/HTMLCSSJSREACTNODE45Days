import { useState } from 'react'

let seq = 1
function createItem(text) {
  const id = globalThis.crypto?.randomUUID?.() ?? `item-${seq++}`
  return { id, text }
}

// TODO(Day38-task01): Track `draft` string state for the text field (initial empty string).
// TODO(Day38-task01): Add `handleAdd` for the button (`type="button"`): if trimmed draft is non-empty, append `createItem(draft)` to `items` and reset `draft` to ''.
// TODO(Day38-task01): Bind the text input as a controlled field using `draft`.
// NOTE: Always render list items with `key={item.id}` (already shown below—do not switch to index keys).
export default function App() {
  const [items, setItems] = useState([createItem('Bread'), createItem('Milk')])

  return (
    <main>
      <h1>Grocery list</h1>
      <ul>
        {items.map((item) => (
          <li key={item.id}>{item.text}</li>
        ))}
      </ul>
      <div className="row">
        <input type="text" placeholder="Add an item" />
        <button type="button">Add</button>
      </div>
    </main>
  )
}
