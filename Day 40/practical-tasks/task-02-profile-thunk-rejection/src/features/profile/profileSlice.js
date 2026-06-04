import { createAsyncThunk, createSlice } from '@reduxjs/toolkit'

export const fetchProfile = createAsyncThunk('profile/fetch', async (_, { rejectWithValue }) => {
  // TODO(Day40-task02): JSONPlaceholder has no user id `0`. Change the URL to fetch **user id 1** successfully.
  const res = await fetch('https://jsonplaceholder.typicode.com/users/0')
  if (!res.ok) return rejectWithValue(`HTTP ${res.status}`)
  return await res.json()
})

const profileSlice = createSlice({
  name: 'profile',
  initialState: {
    user: null,
    status: 'idle',
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    // TODO(Day40-task02): Handle pending/fulfilled/rejected for `fetchProfile`.
    // On fulfilled, store `action.payload` in `user` and return to an idle/succeeded `status` of your choice (match UI expectations below).
    // On rejected, store a helpful `error` string (`action.payload` preferred when present).
  },
})

export default profileSlice.reducer
