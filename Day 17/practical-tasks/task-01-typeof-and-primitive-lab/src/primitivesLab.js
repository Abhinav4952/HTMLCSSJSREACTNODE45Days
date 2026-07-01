/**
 * @param {unknown} value
 * @returns {boolean} true if value is a primitive (including null)
 */
export function isPrimitiveValue(value) {
  if(value === null) return true;
  else if(typeof value==="object" || typeof value==="function") return false;
  return true;
}

/**
 * Return a stable string label for broad typing/debug output.
 * Rules:
 * - `null` -> `"null"`
 * - arrays (`Array.isArray`) -> `"array"`
 * - functions -> `"function"`
 * - plain objects (object not null and not array and not function) -> `"object"`
 * - otherwise return `typeof value` as string (e.g. `"string"`, `"number"`, `"undefined"`, `"boolean"`, `"bigint"`, `"symbol"`)
 */
export function typeLabel(value) {
  if(value===null) return "null";
  else if(Array.isArray(value)) return "array";
  else if(typeof value==="function") return "function";
  else if(typeof value==="object") return "object";

  return typeof value;
}