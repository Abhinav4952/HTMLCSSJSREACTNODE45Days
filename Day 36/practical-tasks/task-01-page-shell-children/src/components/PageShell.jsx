// TODO(Day36-task01): Accept `title` and `children` props.
// TODO(Day36-task01): Render the page title inside the existing `<header><h1>`.
// TODO(Day36-task01): Render `children` inside `<main className="shell__main">` (replace the placeholder paragraph).
export default function PageShell() {
  return (
    <div className="shell">
      <header>
        <h1 style={{ margin: 0, fontSize: '1.25rem' }}>Title placeholder</h1>
      </header>
      <main className="shell__main">
        <p>Replace this placeholder by rendering `children`.</p>
      </main>
      <footer className="shell__footer">© Practice lab</footer>
    </div>
  )
}
