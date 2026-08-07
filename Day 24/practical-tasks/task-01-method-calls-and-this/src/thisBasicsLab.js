/**
 * Factory returning a counter object:
 * - `read()` returns current total
 * - `inc(delta = 1)` increments by finite `delta` (ignore non-finite deltas)
 * Methods must use `this` to read/write the internal counter field `total` on the object.
 */
export function createCounter(initial = 0) {
  return {
    total: initial,
    read() {
      return this.total;
    },
    inc(delta=1) {
      this.total +=(Number.isFinite(delta))?delta:0;
      return this.total;
    },
  };
}
