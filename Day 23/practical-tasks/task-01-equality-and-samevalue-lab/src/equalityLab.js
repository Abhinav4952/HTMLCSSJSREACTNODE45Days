/**
 * Classify the relationship between `a` and `b`:
 * - `"same-value"` when `Object.is(a, b)` is true
 * - `"strict"` when `Object.is` is false but `a === b` is true
 * - `"loose"` when both `Object.is` and `===` are false but `a == b` is true
 * - `"different"` otherwise
 */
export function classifyEquality(a, b) {

  return Object.is(a,b)? "same-value" : (a===b? "strict" : (a==b? "loose" : "different"))
}
