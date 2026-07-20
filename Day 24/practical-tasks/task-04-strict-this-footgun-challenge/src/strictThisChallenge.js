/**
 * Return `typeof this` for a **strict** standalone function invocation (an IIFE).
 */
export function strictStandaloneThisType() {
  return (
    function() {
      "use strict";
      return typeof this;
    }
  )();
}

/**
 * Bind `getter` (a function that reads `this`) to `host` so it can be called later with the correct receiver.
 */
export function bindGetter(getter, host) {
  return getter.bind(host)
}
