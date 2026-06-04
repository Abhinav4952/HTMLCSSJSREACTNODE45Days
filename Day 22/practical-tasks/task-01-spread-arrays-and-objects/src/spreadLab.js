/**
 * Return a new plain object merging enumerable own properties from `base` then `patch` (later wins).
 * - If `base` or `patch` is not a plain object (`Object.prototype` chain), return `null`.
 *   (Treat only objects where `Object.getPrototypeOf(x) === Object.prototype || x` is `Object.create(null)` as plain—tests only use `{}` literals.)
 * - Use object spread at least once.
 */
export function shallowMerge(base, patch) {
  // TODO(Day22-task01): Implement per TASK_INSTRUCTIONS.md
  return null;
}

/**
 * Return `[value, ...list]` when `list` is an array; otherwise return `null`.
 */
export function prepend(list, value) {
  // TODO(Day22-task01): Implement per TASK_INSTRUCTIONS.md
  return null;
}
