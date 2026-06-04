import { configureStore } from '@reduxjs/toolkit'
import detailReducer from '../features/detail/detailSlice.js'

export const store = configureStore({
  reducer: {
    detail: detailReducer,
  },
})
