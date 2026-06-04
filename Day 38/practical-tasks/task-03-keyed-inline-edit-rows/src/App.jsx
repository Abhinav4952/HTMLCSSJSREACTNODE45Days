import { useState } from 'react'

// TODO(Day38-task03): Fix the `key` on each `<li>` — it must remain stable while editing labels.
//       Starter intentionally uses a composite key including `label` which changes every keystroke (bad).
//       Replace it with the stable `item.id` only.
// TODO(Day38-task03): Keep the controlled `<input>` behavior: update `label` immutably for the edited `id`.
export default function App() {
  const [items, setItems] = useState([
    { id: 'row-1', label: 'First' },
    { id: 'row-2', label: 'Second' },
    { id: 'row-3', label: 'Third' },
  ])

  const updateLabel = (id, label) => {
    setItems((prev) => prev.map((item) => (item.id === id ? { ...item, label } : item)))
  }

  return (
    <main>
      <h1>Inline edit rows</h1>
      <p>Type quickly in a field. With a label-derived key, focus may feel jumpy or inputs may remount unnecessarily.</p>
      <ul>
        {items.map((item) => (
          <li key={`${item.id}-${item.label}`}>
            <div className="row">
              <input aria-label={`Edit ${item.id}`} value={item.label} onChange={(e) => updateLabel(item.id, e.target.value)} />
            </div>
          </li>
        ))}
      </ul>
    </main>
  )
}
