/**
 * Classify a value by strict boolean identity vs JS truthiness.
 *
 * Returns:
 * - `"strict-true"` iff `value === true`
 * - `"strict-false"` iff `value === false`
 * - `"truthy"` if not strictly boolean and `Boolean(value)` is true
 * - `"falsy"` otherwise
 */
export function triClassifyBooleaniness(value) {
  
  if(typeof value==="boolean") return `strict-${value}`
  if(value) return "truthy";

  return "falsy";
}
