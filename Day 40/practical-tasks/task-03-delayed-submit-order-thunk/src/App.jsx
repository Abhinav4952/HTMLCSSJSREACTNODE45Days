import CheckoutPanel from './components/CheckoutPanel.jsx'

export default function App() {
  return (
    <main>
      <h1>Delayed submit (`createAsyncThunk`)</h1>
      <p>Implement `extraReducers` so the confirmation id appears after the mocked network delay.</p>
      <CheckoutPanel />
    </main>
  )
}
