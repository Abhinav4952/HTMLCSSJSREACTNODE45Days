import { useDispatch, useSelector } from 'react-redux'
import { resetCheckout, submitOrder } from '../features/orders/orderSlice.js'

const DEMO_LINES = [
  { sku: 'book-1', title: 'Paper notebooks', qty: 1 },
  { sku: 'pen-9', title: 'Gel pens', qty: 2 },
]

export default function CheckoutPanel() {
  const dispatch = useDispatch()
  const { lastConfirmationId, status, error } = useSelector((state) => state.orders)

  return (
    <section>
      <p>
        <button type="button" onClick={() => dispatch(submitOrder(DEMO_LINES))}>
          Submit demo order
        </button>
        <button type="button" style={{ marginLeft: '0.5rem' }} onClick={() => dispatch(resetCheckout())}>
          Reset
        </button>
      </p>
      {status === 'loading' ? <p>Submitting…</p> : null}
      {status === 'failed' ? <p role="alert">Could not submit: {String(error)}</p> : null}
      {lastConfirmationId ? (
        <p>
          <strong>Confirmation:</strong> {lastConfirmationId}
        </p>
      ) : null}
    </section>
  )
}
