/**
 * Return a function equivalent to `fn` with the first argument permanently set to `first`.
 * Must be implemented using `fn.bind(...)`.
 */
export function bindFirstArg(fn, first) {
  return fn.bind(null,first);
}

/**
 * Return `obj.method` bound to `obj` so it can be passed as a callback without losing `this`.
 */
export function bindMethod(obj, methodName) {
  return obj[methodName].bind(obj);
}
