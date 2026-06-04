/**
 * Pick a subset of keys from a plain object using dynamic access.
 *
 * Rules:
 * - If `source` is not a plain object, return `null`.
 * - If `keys` is not an array, return `null`.
 * - For each key in `keys` (in order), if `Object.prototype.hasOwnProperty.call(source, key)`, copy `source[key]`.
 * - Ignore keys not present as own properties.
 */
export function pickOwn(source, keys) {
  // TODO(Day19-task02): Implement per TASK_INSTRUCTIONS.md
  return null;
}

/**
 * Build an object from entries like `[["a", 1], ["b", 2]]`.
 *
 * Rules:
 * - If `entries` is not an array, return `null`.
 * - Ignore non-array rows.
 * - For each row `[k, v]` where `k` is a non-empty string, set `out[k] = v` (later duplicates win).
 */
export function objectFromEntries(entries) {
  // TODO(Day19-task02): Implement per TASK_INSTRUCTIONS.md
  return null;
}
