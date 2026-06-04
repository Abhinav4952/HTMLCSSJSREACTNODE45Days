import { createSelector } from '@reduxjs/toolkit'

export const selectCartItems = (state) => state.cart.items

// TODO(Day39-task04): Implement `selectCartTotalCents` with `createSelector`.
// It should return the sum of `unitPriceCents * qty` across all cart lines.
// Starter returns `0` so the UI shows a placeholder until you finish.
export const selectCartTotalCents = createSelector([selectCartItems], (items) => {
  // TODO(Day39-task04): Replace this placeholder return with the sum of `unitPriceCents * qty` for each line in `items`.
  return 0
})
