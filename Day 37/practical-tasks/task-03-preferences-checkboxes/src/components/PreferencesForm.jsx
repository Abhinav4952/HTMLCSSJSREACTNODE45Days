import { useState } from 'react'

const initial = { email: false, sms: false, weeklyDigest: false }

// TODO(Day37-task03): Wire each checkbox `onChange` to flip the correct boolean in `prefs` immutably.
// TODO(Day37-task03): Replace the summary text with a live sentence listing enabled channels (human readable).
export default function PreferencesForm() {
  const [prefs, setPrefs] = useState(initial)

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault()
      }}
    >
      <fieldset>
        <legend>Channels</legend>
        <label className="row">
          <input type="checkbox" checked={prefs.email} onChange={() => {}} />
          Product email digests
        </label>
        <label className="row">
          <input type="checkbox" checked={prefs.sms} onChange={() => {}} />
          SMS for outages
        </label>
        <label className="row">
          <input type="checkbox" checked={prefs.weeklyDigest} onChange={() => {}} />
          Weekly study plan
        </label>
      </fieldset>
      <div className="summary" aria-live="polite">
        Summary placeholder — complete TODOs.
      </div>
    </form>
  )
}
