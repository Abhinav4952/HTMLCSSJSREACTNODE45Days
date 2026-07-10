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

  if(typeof n ==="number") {
    if(Number.isNaN(n)) return "nan";
    else if(!Number.isFinite(n)) return "other";
    else if(n>0) return "positive"; 
    else if(n<0) return "negative";
    else return "zero";
  }
  return "other";
}
