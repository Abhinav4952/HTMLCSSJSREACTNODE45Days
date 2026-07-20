/**
 * Given an array of pairs `[[a,b], ...]`, return a new array of sums `a + b`.
 * Rules:
 * - If `pairs` is not an array, return `null`.
 * - For each pair, if an entry is missing or not a finite number, treat that entry as `0`.
 * - Implement using `Array.prototype.map` and an **arrow function** callback (no `function` keyword inside `map`).
 */
export function sumPairs(pairs) {
  if (!Array.isArray(pairs)) {
    return null;
  }

  return pairs.map(pair => {
    const a = Number.isFinite(pair?.[0]) ? pair[0] : 0;
    const b = Number.isFinite(pair?.[1]) ? pair[1] : 0;

    return a + b;
  });
}
/**
 * Returns `(x) => x + scale` as an arrow function.
 * - If `x` is not a finite number, return `NaN`.
 */
export function makeScaledAdder(scale) {

  if(Number.isFinite(scale)) return (x)=> x+scale;

  return () => Number.NaN;
}
