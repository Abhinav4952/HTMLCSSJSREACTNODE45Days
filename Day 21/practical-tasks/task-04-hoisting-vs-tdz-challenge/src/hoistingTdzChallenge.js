/**
 * Return the tuple `[typeof x, x]` observed **before** the `var x = 1` initializer runs
 * inside a nested function body (classic `var` hoisting demonstration).
 */
export function varBindingBeforeInit() {
    function inner() {
        return [typeof x, x];
        var x = 1;
    }

    return inner();
}
/**
 * Return `true` if probing a `let` binding in its TDZ throws `ReferenceError`, else `false`.
 *
 * Implement by declaring a nested function that touches `y` before `let y = 1`, invoking it inside `try/catch`.
 */
export function letBindingThrowsInTdz() {
    function inner() {
        console.log(y);
        let y = 1;
    }
    try {
        inner();
        return false;
    } catch (e) {
        return e instanceof ReferenceError;
    }
  return false;
}

/**
 * Challenge: implement `safeDelay(fn, ms = 0)` that returns a function calling `fn` after `ms` milliseconds
 * using `setTimeout` **without** invoking `fn` synchronously.
 * For this autograder, **do not rely on real timers**: instead, capture the callback passed to `setTimeout`
 * and return `{ schedule, flush }` where:
 * - `schedule()` calls `setTimeout` with the wrapped call (you may assume global `setTimeout` exists).
 * - `flush()` invokes the captured callback immediately to make tests deterministic.
 *
 * This is a **pattern** exercise: build a tiny test seam around async scheduling.
 */
export function createTimeoutHarness(fn, ms = 0) {
    let callback;

    return {
        schedule() {
          callback= ()=> fn()
            setTimeout(callback, ms);
        },

        flush() {
            if (callback) callback();
        }
    };
}
