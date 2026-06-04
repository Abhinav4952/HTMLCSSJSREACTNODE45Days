/**
 * Build a display label from string parts.
 *
 * Rules:
 * - If `parts` is not an array, return `null`.
 * - Trim each entry; drop entries that become empty strings.
 * - Join remaining entries with `separator` (use default ` " | "` when argument is omitted).
 * - If nothing remains, return `emptyFallback` (default `"(none)"`).
 * - Defaults must be implemented with **ES2015 default parameters** on `separator` and `emptyFallback` (not manual `undefined` checks for those two).
 */
export function buildLabel(parts, separator = " | ", emptyFallback = "(none)") {
  // TODO(Day21-task03): Implement per TASK_INSTRUCTIONS.md
  return null;
}

/**
 * `repeatText(text, times = 1)` returns `text` repeated `times` times as one string.
 * - If `text` is not a string, return `""`.
 * - `times` must be an integer in `[0, 5]`; if invalid, treat as `1` (still use default parameter feature for the binding, but you may clamp after receiving args).
 */
export function repeatText(text, times = 1) {
  // TODO(Day21-task03): Implement per TASK_INSTRUCTIONS.md
  return "";
}
