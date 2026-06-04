// TODO(Day35-task01): Import `useState` from `react`.
// TODO(Day35-task01): Store an integer count starting at `0`.
// TODO(Day35-task01): Render the current count inside <output> (below).
// TODO(Day35-task01): Wire buttons: "+1" increments, "-1" decrements, "Reset" returns to 0.
// TODO(Day35-task01): Use `type="button"` on all buttons.
export default function Counter() {
  return (
    <section className="counter">
      <output aria-live="polite">0</output>
      <div className="row">
        <button type="button">+1</button>
        <button type="button">-1</button>
        <button type="button">Reset</button>
      </div>
    </section>
  )
}
