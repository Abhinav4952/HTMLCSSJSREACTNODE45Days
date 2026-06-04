/**
 * @param {unknown} value
 * @returns {boolean} true if value is a primitive (including null)
 */
export function isPrimitiveValue(value) {
  // TODO(Day17-task01): Implement per TASK_INSTRUCTIONS.md
  return false;
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
  // TODO(Day17-task01): Implement per TASK_INSTRUCTIONS.md
  return "object";
}
