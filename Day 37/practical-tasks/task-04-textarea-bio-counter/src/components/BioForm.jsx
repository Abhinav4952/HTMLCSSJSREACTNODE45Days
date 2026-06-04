const MAX = 140

// TODO(Day37-task04): Import `useState` from `react` when you begin implementation.
// TODO(Day37-task04): Render a controlled `<textarea>` with `maxLength={MAX}`.
// TODO(Day37-task04): Show remaining characters: `Remaining: N` where N updates as the user types.
// TODO(Day37-task04): Add subtle styling: when remaining < 20, add class `warn` to the remaining `<span>`; when remaining === 0, use `danger` instead.
export default function BioForm() {
  return (
    <form
      onSubmit={(e) => {
        e.preventDefault()
      }}
    >
      <label htmlFor="bio">Bio ({MAX} characters max)</label>
      <textarea id="bio" name="bio" placeholder="Tell attendees what to expect..." />
      <div className="meta">
        <span>Remaining: {MAX}</span>
      </div>
    </form>
  )
}
