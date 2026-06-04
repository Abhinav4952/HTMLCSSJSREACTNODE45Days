/**
 * Factory returning a counter object:
 * - `read()` returns current total
 * - `inc(delta = 1)` increments by finite `delta` (ignore non-finite deltas)
 * Methods must use `this` to read/write the internal counter field `total` on the object.
 */
export function createCounter(initial = 0) {
  // TODO(Day24-task01): Implement per TASK_INSTRUCTIONS.md
  return {
    total: Number.NaN,
    read() {
      return this.total;
    },
    inc() {
      return this.total;
    },
  };
}
