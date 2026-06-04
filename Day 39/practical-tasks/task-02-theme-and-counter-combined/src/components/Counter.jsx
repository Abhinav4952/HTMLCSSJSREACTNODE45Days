import { useDispatch, useSelector } from 'react-redux'
import { decrement, increment, reset } from '../features/counter/counterSlice.js'

export default function Counter() {
  const value = useSelector((state) => state.counter.value)
  const dispatch = useDispatch()

  return (
    <section>
      <output aria-live="polite" style={{ display: 'block', fontSize: '2rem', fontWeight: 700, marginBottom: '0.75rem' }}>
        {value}
      </output>
      <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
        <button type="button" onClick={() => dispatch(increment())}>
          +1
        </button>
        <button type="button" onClick={() => dispatch(decrement())}>
          -1
        </button>
        <button type="button" onClick={() => dispatch(reset())}>
          Reset
        </button>
      </div>
    </section>
  )
}
