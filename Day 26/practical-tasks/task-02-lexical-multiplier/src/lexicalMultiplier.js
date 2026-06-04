/**
 * Return `(x) => x * scale` where `scale` is captured from the outer call.
 * - If `scale` is not a finite number, return a function that always returns `NaN`.
 */
export function makeMultiplier(scale) {
  // TODO(Day26-task02): Implement per TASK_INSTRUCTIONS.md
  return () => Number.NaN;
}
