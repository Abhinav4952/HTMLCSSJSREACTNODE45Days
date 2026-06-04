import { useDispatch, useSelector } from 'react-redux'
import { toggleMode } from '../features/theme/themeSlice.js'

export default function ThemeToggle() {
  const mode = useSelector((state) => state.theme.mode)
  const dispatch = useDispatch()

  return (
    <section style={{ marginBottom: '1.25rem' }}>
      <p style={{ marginTop: 0 }}>
        Current theme: <strong>{mode}</strong>
      </p>
      <button type="button" onClick={() => dispatch(toggleMode())}>
        Toggle theme
      </button>
    </section>
  )
}
