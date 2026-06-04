# Task 3 — Class timer: mount + unmount cleanup

## Summary

Implement a **class component** timer that increments every second while mounted, and **clears the interval** on unmount. `App.jsx` mounts/unmounts the timer so you can manually verify cleanup in DevTools and by watching the console (optional).

## Learning goals

- Use **`componentDidMount`** to start a browser timer.
- Use **`componentWillUnmount`** to release resources.
- Prefer **functional `setState`** updates for interval ticks.

## Provided files

- `src/components/TicketTimer.jsx` — edit surface.
- `src/App.jsx` — mount toggle (read-only).

## What you will implement

1. `tick` increments `seconds` once per second via `setInterval`.
2. Interval cleared on unmount (no runaway timers after unmount).

## How to run and verify

```bash
cd "Day 35/practical-tasks/task-03-class-timer-lifecycle"
npm install
npm run dev
```

Optional: `npm run build`.

### Manual checks

- [ ] While mounted, seconds increase roughly every real second.
- [ ] Click **Unmount timer** — counter stops increasing (watch for ~5s).
- [ ] Mount again — counter resets to 0 on fresh mount (acceptable) OR continues—**either behavior is OK** as long as no duplicate intervals fire; simplest is reset on remount via constructor initial state (default React remount creates new instance → seconds reset to 0).

## `TODO` map

| `TicketTimer.jsx` | Done means |
|---------------------|------------|
| `componentDidMount` | Starts interval calling `tick`. |
| `tick` | Functional `setState` increment. |
| `componentWillUnmount` | Clears interval. |

## Submission checklist (Git)

- [ ] Only TODO-marked files changed (`TicketTimer.jsx`).
