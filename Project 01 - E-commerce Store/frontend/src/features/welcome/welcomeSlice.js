import { createAsyncThunk, createSlice } from '@reduxjs/toolkit'
import { apiRequest } from '../../api/client'

/**
 * Sample Redux Toolkit slice.
 * Pattern for candidates: createAsyncThunk for API calls + slice for status/data/error.
 * Later: authSlice, cartSlice / booksSlice, etc.
 */
export const fetchWelcome = createAsyncThunk('welcome/fetch', async () => {
  return apiRequest('/api/welcome')
})

const welcomeSlice = createSlice({
  name: 'welcome',
  initialState: {
    message: '',
    status: 'idle', // idle | loading | succeeded | failed
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchWelcome.pending, (state) => {
        state.status = 'loading'
        state.error = null
      })
      .addCase(fetchWelcome.fulfilled, (state, action) => {
        state.status = 'succeeded'
        state.message = action.payload.message || 'Welcome to the E-commerce Store'
      })
      .addCase(fetchWelcome.rejected, (state, action) => {
        state.status = 'failed'
        state.error = action.error.message || 'Failed to load welcome message'
      })
  },
})

export default welcomeSlice.reducer
