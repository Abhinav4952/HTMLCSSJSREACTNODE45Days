import { useDispatch, useSelector } from 'react-redux'
import { fetchProfile } from '../features/profile/profileSlice.js'

export default function ProfilePanel() {
  const dispatch = useDispatch()
  const { user, status, error } = useSelector((state) => state.profile)

  return (
    <section>
      <button type="button" onClick={() => dispatch(fetchProfile())}>
        Load profile
      </button>
      {status === 'loading' ? <p>Loading…</p> : null}
      {status === 'failed' ? <p role="alert">Error: {String(error)}</p> : null}
      {user ? (
        <div style={{ marginTop: '1rem' }}>
          <p>
            <strong>Name:</strong> {user.name}
          </p>
          <p>
            <strong>Email:</strong> {user.email}
          </p>
        </div>
      ) : null}
    </section>
  )
}
