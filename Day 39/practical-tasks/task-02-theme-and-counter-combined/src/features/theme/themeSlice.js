import { createSlice } from '@reduxjs/toolkit'

const themeSlice = createSlice({
  name: 'theme',
  initialState: { mode: 'light' },
  reducers: {
    toggleMode: (state) => {
      // TODO(Day39-task02): Toggle `state.mode` between `'light'` and `'dark'` only (no other strings).
    },
  },
})

export const { toggleMode } = themeSlice.actions
export default themeSlice.reducer
