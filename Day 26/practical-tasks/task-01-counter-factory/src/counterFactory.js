/**
 * Return an object API `{ read, inc, reset }` backed by **private** mutable state (closure).
 * - `read()` returns the current integer total.
 * - `inc(delta = 1)` adds `delta` if `delta` is a finite number; otherwise ignores.
 * - `reset()` sets total back to `initial` (the value passed when `createCounter` was called).
 */
export function createCounter(initial = 0) {
  let val = initial;

  return {
    read() {return val;},

    inc(delta = 1) {
      if(Number.isFinite(delta))
        val+=delta
      return val;
    },

    reset(){
      val = initial;
    }
  }
}
