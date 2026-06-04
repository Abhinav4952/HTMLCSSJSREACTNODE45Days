/**
 * Convert common “user-ish” inputs into an integer, or return null if conversion is unsafe/invalid.
 *
 * Rules:
 * - `null` or `undefined` -> `null`
 * - `true` -> `1`, `false` -> `0`
 * - finite numbers -> `Math.trunc` toward zero
 * - strings -> trim; if empty -> `null`; else parse as base-10 integer (reject if parse is NaN)
 * - anything else -> `null`
 *
 * Reject:
 * - non-finite numbers (`NaN`, `Infinity`, `-Infinity`)
 * - strings that are not valid integer strings after trim (e.g. `"12px"`, `"12.3"`)
 */
export function toIntegerOrNull(value) {
  // TODO(Day17-task04): Implement per TASK_INSTRUCTIONS.md
  return null;
}

/**
 * JSON.stringify for objects/arrays; otherwise String(value).
 * - `undefined` alone should stringify as `"undefined"` (use String)
 */
export function stringifyForLog(value) {
  // TODO(Day17-task04): Implement per TASK_INSTRUCTIONS.md
  return "";
}
