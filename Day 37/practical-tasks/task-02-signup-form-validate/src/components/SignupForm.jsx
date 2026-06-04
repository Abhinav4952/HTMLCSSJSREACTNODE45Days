import { useMemo } from 'react'

function validate({ fullName, email, password }) {
  const errors = {}
  if (!fullName.trim()) errors.fullName = 'Full name is required.'
  if (!email.trim()) errors.email = 'Email is required.'
  else if (!email.includes('@')) errors.email = 'Email must contain "@".'
  if (!password) errors.password = 'Password is required.'
  else if (password.length < 8) errors.password = 'Password must be at least 8 characters.'
  return errors
}

// TODO(Day37-task02): Track `fullName`, `email`, and `password` with `useState` (three strings).
// TODO(Day37-task02): On each render, derive `errors` using the provided `validate` helper (use `useMemo` keyed on the three fields).
// TODO(Day37-task02): Disable the submit button when `Object.keys(errors).length > 0`.
// TODO(Day37-task02): Controlled inputs: wire `value` + `onChange` for all three fields.
// TODO(Day37-task02): Render error text under a field when `errors.fieldName` exists (use <p className="error" role="alert">).
// TODO(Day37-task02): On valid submit, `preventDefault` and `alert` a short success message (no backend).
export default function SignupForm() {
  const errors = useMemo(() => validate({ fullName: '', email: '', password: '' }), [])

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault()
      }}
    >
      <div>
        <label htmlFor="fullName">Full name</label>
        <input id="fullName" name="fullName" autoComplete="name" />
      </div>
      <div>
        <label htmlFor="email">Email</label>
        <input id="email" name="email" type="email" autoComplete="email" />
      </div>
      <div>
        <label htmlFor="password">Password</label>
        <input id="password" name="password" type="password" autoComplete="new-password" />
      </div>
      <button type="submit" disabled={Object.keys(errors).length > 0}>
        Create account
      </button>
    </form>
  )
}
