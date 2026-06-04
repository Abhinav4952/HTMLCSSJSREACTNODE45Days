import { configureStore } from '@reduxjs/toolkit'
import counterReducer from '../features/counter/counterSlice.js'
import themeReducer from '../features/theme/themeSlice.js'

export const store = configureStore({
  reducer: {
    counter: counterReducer,
    theme: themeReducer,
  },
})
