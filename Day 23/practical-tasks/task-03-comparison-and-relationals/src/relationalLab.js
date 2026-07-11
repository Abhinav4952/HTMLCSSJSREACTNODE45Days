/**
 * Lexicographic `>` for two strings (relational comparison, no numeric coercion).
 * Return `null` if either operand is not a string.
 */
export function isLexicographicGreater(a, b) {
  if(typeof a==="string" && typeof b==="string") return a>b;
  return null;
}

/**
 * Numeric `>` after coercing both operands with `Number(...)`.
 * Return `null` if either coercion is not a finite number.
 */
export function isNumericGreater(a, b) {
  if(Number.isFinite(Number(a)) && Number.isFinite(Number(b))) return Number(a)>Number(b);
  return null;
}
