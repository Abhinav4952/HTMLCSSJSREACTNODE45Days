/**
 * Like `Array.prototype.map`, but require `items` to be an array.
 * - If `items` is not an array, return `null`.
 * - Otherwise return a new array where each element is `fn(item, index)`.
 */
export function mapWith(items, fn) {
  if(Array.isArray(items)) {
    return items.map((item,i)=>fn(item,i));
  }
  return null;
}

/**
 * Return a function that invokes `predicate` and returns the opposite boolean coerced with `Boolean`.
 */
export function negate(predicate) {

  return (...args) => !predicate(...args);
}
