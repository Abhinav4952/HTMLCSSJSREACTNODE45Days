import { createSlice } from '@reduxjs/toolkit'

const counterSlice = createSlice({
  name: 'counter',
  initialState: { value: 0 },
  reducers: {
    increment: (state) => {
      // TODO(Day39-task01): Increase `state.value` by 1 (RTK + Immer allows direct mutation syntax).
    },
    decrement: (state) => {
      // TODO(Day39-task01): Decrease `state.value` by 1, but **do not** go below 0 (clamp at 0).
    },
    reset: (state) => {
      // TODO(Day39-task01): Reset `state.value` to 0.
    },
  },
})

export const { increment, decrement, reset } = counterSlice.actions
export default counterSlice.reducer
