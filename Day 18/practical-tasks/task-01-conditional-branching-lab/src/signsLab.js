/**
 * Classify numeric sign for dashboard coloring.
 *
 * Rules:
 * - If `n` is not of type `"number"`, return `"other"`.
 * - `NaN` -> `"nan"`
 * - `Infinity` or `-Infinity` -> `"other"`
 * - `0` or `-0` -> `"zero"`
 * - positive -> `"positive"`
 * - negative -> `"negative"`
 */
export function signCategory(n) {
  // TODO(Day18-task01): Implement per TASK_INSTRUCTIONS.md
  return "other";
}
