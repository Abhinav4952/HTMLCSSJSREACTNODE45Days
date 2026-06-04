import { useSelector } from 'react-redux'
import { selectCartItems, selectCartTotalCents } from '../features/cart/cartSelectors.js'

function formatMoney(cents) {
  return new Intl.NumberFormat(undefined, { style: 'currency', currency: 'USD' }).format(cents / 100)
}

export default function CartView() {
  const items = useSelector(selectCartItems)
  const totalCents = useSelector(selectCartTotalCents)

  return (
    <section>
      <h2 style={{ marginTop: 0 }}>Cart</h2>
      <ul>
        {items.map((line) => (
          <li key={line.id}>
            {line.title} × {line.qty} @ {formatMoney(line.unitPriceCents)} each
          </li>
        ))}
      </ul>
      <p>
        <strong>Total:</strong> {formatMoney(totalCents)}
      </p>
      <p style={{ color: '#64748b', fontSize: '0.95rem' }}>
        Expected total for the seeded lines: <code>$18.97</code> (verify after your selector is correct).
      </p>
    </section>
  )
}
