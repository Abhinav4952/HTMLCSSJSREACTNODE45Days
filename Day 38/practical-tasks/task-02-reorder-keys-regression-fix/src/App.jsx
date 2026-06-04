import { useState } from 'react'

function moveIndex(list, from, to) {
  if (to < 0 || to >= list.length) return list
  const next = [...list]
  const [removed] = next.splice(from, 1)
  next.splice(to, 0, removed)
  return next
}

// TODO(Day38-task02): Replace `key={index}` with a stable key from each item (use `item.id`).
export default function App() {
  const [items, setItems] = useState([
    { id: 'seed-a', label: 'Apples' },
    { id: 'seed-b', label: 'Bananas' },
    { id: 'seed-c', label: 'Carrots' },
  ])

  const updateLabel = (id, label) => {
    setItems((prev) => prev.map((item) => (item.id === id ? { ...item, label } : item)))
  }

  return (
    <main>
      <h1>Reorder + controlled rows</h1>
      <p>
        Use <strong>Move up</strong>/<strong>Move down</strong> while editing text. With index keys, labels can appear to “jump”
        between rows. Fixing keys should stabilize identity.
      </p>
      <ol>
        {items.map((item, index) => (
          <li key={index}>
            <div className="row">
              <input
                aria-label={`Label for row ${index + 1}`}
                value={item.label}
                onChange={(e) => updateLabel(item.id, e.target.value)}
              />
              <button
                type="button"
                onClick={() => setItems((prev) => moveIndex(prev, index, index - 1))}
              >
                Move up
              </button>
              <button
                type="button"
                onClick={() => setItems((prev) => moveIndex(prev, index, index + 1))}
              >
                Move down
              </button>
            </div>
          </li>
        ))}
      </ol>
    </main>
  )
}
