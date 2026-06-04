# Evaluation Criteria — Day 35 — Task 3 — Class timer lifecycle

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 50 | Interval increments; cleared on unmount. |
| Lifecycle usage | 30 | Correct methods; id stored on instance. |
| State updates | 20 | Functional `setState` in tick. |

## Pass / fail gates

- Timer keeps incrementing after unmount (cleanup missing).
- Build fails.

## Evidence

- Short screen recording or step-by-step notes showing unmount stops updates.

## AI grading prompt

Verify `TicketTimer.jsx` uses `setInterval` in mount, `clearInterval` in unmount, and functional `setState` in tick.
