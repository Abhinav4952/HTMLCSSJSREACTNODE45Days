/**
 * Return `{ first, restSum }` where `restSum` is the sum of all **finite numbers** in `...rest`.
 * - If `first` is not a finite number, return `null`.
 * - Ignore non-numbers in `rest`.
 * - Must use a **rest parameter** (`...rest`) in the function signature.
 */
export function firstAndRestSum(first, ...rest) {
  if(Number.isFinite(first)) {
    let restSum=0;
    for(let val of rest) {
      if(typeof val==="number" && Number.isFinite(val))
        restSum+=val;
    }
    return {first,restSum}
  }
  return null;
}

/**
 * Forward variadic args to `Math.max` using spread in the call.
 * - If no finite numbers provided across all args, return `NaN`.
 * - If any arg is not a finite number, ignore it.
 */
export function maxFinite(...values) {
  values.filter(val=> Number.isFinite(val));
  if(values.length!==0) {
    return Math.max(...values);
  } 
  return Number.NaN;
}
