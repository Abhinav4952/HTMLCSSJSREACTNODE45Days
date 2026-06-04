import { createAsyncThunk, createSlice } from '@reduxjs/toolkit'

export const fetchPosts = createAsyncThunk('posts/fetchPosts', async (_, { rejectWithValue }) => {
  const res = await fetch('https://jsonplaceholder.typicode.com/posts?_limit=5')
  if (!res.ok) return rejectWithValue(`HTTP ${res.status}`)
  return await res.json()
})

const postsSlice = createSlice({
  name: 'posts',
  initialState: {
    items: [],
    status: 'idle',
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    // TODO(Day40-task01): Handle `fetchPosts.pending` — set `status` to `'loading'` and clear `error`.
    // TODO(Day40-task01): Handle `fetchPosts.fulfilled` — set `items` to `action.payload`, `status` to `'idle'` (or `'succeeded'` if you prefer, but keep it consistent in UI), clear `error`.
    // TODO(Day40-task01): Handle `fetchPosts.rejected` — set `status` to `'failed'` and set `error` to a useful string (`action.payload` if present, else `action.error.message`).
  },
})

export default postsSlice.reducer
