/**
 * Create a tiny counter API as a plain object with methods (closure-based state is OK).
 *
 * Requirements:
 * - `read()` returns the current integer total.
 * - `add(delta = 1)` increments total by `delta`.
 * - `reset(value = 0)` sets total to `value` if `value` is a finite number; otherwise sets to `0`.
 * - Initial total is `start` if it is a finite number, else `0`.
 */
export function createCounter(start = 0) {
  let total = (Number.isFinite(start)? start:0);
  return {
    read() {
      return total;
    },
    add(delta=1) {total+=delta;},
    reset(value) {total = (Number.isFinite(value))? value : 0;},
  };
}
