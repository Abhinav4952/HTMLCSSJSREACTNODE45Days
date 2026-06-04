import { configureStore } from '@reduxjs/toolkit'
import ordersReducer from '../features/orders/orderSlice.js'

export const store = configureStore({
  reducer: {
    orders: ordersReducer,
  },
})
