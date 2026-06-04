import { createSlice } from '@reduxjs/toolkit'

const cartSlice = createSlice({
  name: 'cart',
  initialState: {
    items: [
      { id: 'line-1', title: 'Notebook', unitPriceCents: 499, qty: 2 },
      { id: 'line-2', title: 'Pen pack', unitPriceCents: 899, qty: 1 },
    ],
  },
  reducers: {},
})

export default cartSlice.reducer
