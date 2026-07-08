/**
 * Return the last `n` elements as a new array (or fewer if `arr` is shorter).
 *
 * Rules:
 * - If `arr` is not an array, return `null`.
 * - If `n` is not a finite integer or `n < 0`, return `null`.
 * - If `n === 0`, return `[]`.
 */
export function tail(arr, n) {

  if(Array.isArray(arr) && Number.isFinite(n) && Number.isInteger(n) && n>=0) {
    console.log("Entered first if")
    if(n>arr.length) return arr;
    console.log("Bypassed second if")

    return arr.splice(arr.length-n,n);
  }

  return null;
}

/**
 * Return the first index `i` such that `arr[i] > threshold` using strict `>` comparisons.
 *
 * Rules:
 * - If `arr` is not an array, return `null`.
 * - If `threshold` is not a finite number, return `null`.
 * - If no element satisfies, return `-1`.
 * - Ignore non-finite elements while scanning (treat them as not `> threshold`).
 */
export function firstIndexGreaterThan(arr, threshold) {
  if(Array.isArray(arr) && Number.isFinite(threshold)) {
    let res = arr.findIndex(x=>Number.isFinite(x) && x>threshold);
    return res;
  }
  return null;
}

console.log(tail(null,1))
