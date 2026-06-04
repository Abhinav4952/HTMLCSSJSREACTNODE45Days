/**
 * Create a memoized summer over **plain objects** whose own enumerable values are finite numbers.
 *
 * Requirements:
 * - `sum(cfg)` returns the sum of finite numeric values in `cfg` (ignore non-numbers / non-finite).
 * - If `cfg` is not a plain object (same rule as Day 22: only `{}` literals / `Object.create(null)` in tests), return `null`.
 * - Cache results so logically-equal configs with different **key insertion order** still hit the cache.
 * - Expose `misses()` counting how many times the expensive aggregation ran (cache misses).
 */
export function createCachedNumericSum() {
  // TODO(Day25-task04): Implement per TASK_INSTRUCTIONS.md
  return {
    sum() {
      return null;
    },
    misses() {
      return 0;
    },
  };
}
