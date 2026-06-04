import { useState } from 'react'

// TODO(Day37-task01): Store email string in `useState` with initial empty string.
// TODO(Day37-task01): Render a labeled `<input type="email">` that is **controlled** via `value` + `onChange`.
// TODO(Day37-task01): Show a read-only hint line under the field echoing the current value: `Current value: ...` (empty string ok).
export default function EmailField() {
  return (
    <form
      onSubmit={(e) => {
        e.preventDefault()
      }}
    >
      <label htmlFor="email">Email</label>
      <input id="email" name="email" type="email" placeholder="you@example.com" />
      <p className="hint">Current value: (complete TODOs)</p>
    </form>
  )
}
