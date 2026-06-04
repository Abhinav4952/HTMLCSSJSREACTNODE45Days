import { createAsyncThunk, createSlice } from '@reduxjs/toolkit'

export const submitOrder = createAsyncThunk('orders/submit', async (lines, { rejectWithValue }) => {
  await new Promise((resolve) => setTimeout(resolve, 500))
  if (!Array.isArray(lines) || lines.length === 0) return rejectWithValue('Cart is empty')
  return { confirmationId: `DEMO-${Date.now().toString(36).toUpperCase()}` }
})

const orderSlice = createSlice({
  name: 'orders',
  initialState: {
    lastConfirmationId: null,
    status: 'idle',
    error: null,
  },
  reducers: {
    resetCheckout: (state) => {
      state.lastConfirmationId = null
      state.status = 'idle'
      state.error = null
    },
  },
  extraReducers: (builder) => {
    // TODO(Day40-task03): Handle pending/fulfilled/rejected for `submitOrder`.
    // On fulfilled, store `action.payload.confirmationId` in `lastConfirmationId`, clear `error`, and return `status` to a non-loading state.
    // On rejected, set `error` and failed-ish `status` consistent with your UI checks in `CheckoutPanel.jsx`.
  },
})

export const { resetCheckout } = orderSlice.actions
export default orderSlice.reducer
