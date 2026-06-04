// TODO(Day35-task02): Import `useState` from `react`.
// TODO(Day35-task02): Track whether the panel body is open (boolean). Start **closed** (`false`).
// TODO(Day35-task02): Render a button next to the title that toggles open/closed on click (`type="button"`).
// TODO(Day35-task02): The button label should reflect state, e.g. "Show" when closed and "Hide" when open (or similar clear wording).
// TODO(Day35-task02): Only render `props.children` inside the `<div className="panel__body">` when open. When closed, omit the body div entirely (no empty bordered box).
export default function DisclosurePanel({ title, children }) {
  return (
    <section className="panel">
      <header style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '0.75rem' }}>
        <h2 style={{ margin: 0, fontSize: '1.1rem' }}>{title}</h2>
        <button type="button">Toggle</button>
      </header>
    </section>
  )
}
