import { createAsyncThunk, createSlice } from '@reduxjs/toolkit'

export const fetchPostBundle = createAsyncThunk('detail/fetchBundle', async (postId, { rejectWithValue }) => {
  const [postRes, commentsRes] = await Promise.all([
    fetch(`https://jsonplaceholder.typicode.com/posts/${postId}`),
    fetch(`https://jsonplaceholder.typicode.com/posts/${postId}/comments`),
  ])
  if (!postRes.ok) return rejectWithValue(`post HTTP ${postRes.status}`)
  if (!commentsRes.ok) return rejectWithValue(`comments HTTP ${commentsRes.status}`)
  const post = await postRes.json()
  const comments = await commentsRes.json()
  return { post, comments }
})

const detailSlice = createSlice({
  name: 'detail',
  initialState: {
    post: null,
    comments: [],
    status: 'idle',
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    // TODO(Day40-task04): Handle pending/fulfilled/rejected for `fetchPostBundle`.
    // On fulfilled, store `action.payload.post` and `action.payload.comments`, clear `error`, and set `status` so the UI stops showing loading.
    // On rejected, populate `error` and a failed `status` consistent with `PostExplorer.jsx`.
  },
})

export default detailSlice.reducer
