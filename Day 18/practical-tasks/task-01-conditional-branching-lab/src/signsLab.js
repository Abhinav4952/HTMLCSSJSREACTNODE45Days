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
  return "other";
}
