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
  if (value===null || value === undefined) {
    return null;
  }

  if (value=== true) return 1;
  if (value=== false) return 0;

  if (typeof value ==="number") {
    if (!Number.isFinite(value)) return null;
    return Math.trunc(value);
  }

  if (typeof value === "string") {
  value = value.trim();

  if (value==="") return null;

  const num = Number(value);

  if (!Number.isInteger(num)) return null;

  return num;
}

  return null;
}

/**
 * JSON.stringify for objects/arrays; otherwise String(value).
 * - `undefined` alone should stringify as `"undefined"` (use String)
 */
export function stringifyForLog(value) {
  if(typeof value==="object") return JSON.stringify(value);
  return String(value);
}
