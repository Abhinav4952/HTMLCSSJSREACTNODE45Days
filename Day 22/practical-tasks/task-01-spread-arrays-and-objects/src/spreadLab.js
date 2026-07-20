/**
 * Return a new plain object merging enumerable own properties from `base` then `patch` (later wins).
 * - If `base` or `patch` is not a plain object (`Object.prototype` chain), return `null`.
 *   (Treat only objects where `Object.getPrototypeOf(x) === Object.prototype || x` is `Object.create(null)` as plain—tests only use `{}` literals.)
 * - Use object spread at least once.
 */

function isPlainObject(x){
  if(x===null) return false;
  let p= Object.getPrototypeOf(x)
  return p===Object.prototype || p===null;
}

export function shallowMerge(base, patch) {
  if(isPlainObject(base)  && isPlainObject(patch)) {
    return {...base,...patch}
  }
  return null;
}

/**
 * Return `[value, ...list]` when `list` is an array; otherwise return `null`.
 */
export function prepend(list, value) {
  if(Array.isArray(list)) {
    return [value,...list]
  }
  return null;
}
