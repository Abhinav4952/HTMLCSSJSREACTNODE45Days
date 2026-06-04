import { configureStore } from '@reduxjs/toolkit'
import profileReducer from '../features/profile/profileSlice.js'

export const store = configureStore({
  reducer: {
    profile: profileReducer,
  },
})
