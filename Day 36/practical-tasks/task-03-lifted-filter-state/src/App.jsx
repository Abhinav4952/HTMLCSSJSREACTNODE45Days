import { useState } from 'react'
import { PRODUCTS } from './data/products.js'
import ProductList from './components/ProductList.jsx'
import SearchField from './components/SearchField.jsx'

export default function App() {
  const [query, setQuery] = useState('')

  // TODO(Day36-task03): Pass a real `onChange` handler into `SearchField` so typing updates `query` via `setQuery`.
  // Hint: reuse the same handler function in the prop (do not leave a no-op).

  return (
    <main>
      <h1>Inventory search</h1>
      <SearchField value={query} onChange={() => {}} />
      <ProductList products={PRODUCTS} query={query} />
    </main>
  )
}
