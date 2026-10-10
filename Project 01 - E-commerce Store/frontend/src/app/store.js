import { configureStore } from '@reduxjs/toolkit'
import welcomeReducer from '../features/welcome/welcomeSlice'

/**
 * Redux store.
 * Candidates: add more reducers (auth, cart/products/orders or books/loans).
 */
export const store = configureStore({
  reducer: {
    welcome: welcomeReducer,
  },
})
