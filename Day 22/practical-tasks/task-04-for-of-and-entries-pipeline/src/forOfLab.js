/**
 * Multiply all **finite numeric** own property values on a plain object using `for...of` over `Object.values`.
 * - If `record` is not an object or is `null`, return `null`.
 * - If there are no finite numeric values, return `null`.
 */
export function productOfNumericValues(record) {
  if(record!==null && typeof record==="object") {
    let res=1;
    let flag=false;
    for(const val of Object.values(record)) {
      if(Number.isFinite(val)) {
        flag=true;
        res *=val;
      }
    }
    if(flag) return res;
  }
  return null;
}

/**
 * Given an array of `[key, value]` pairs, sum all finite numeric `value`s using `for...of` over the array.
 * - If `entries` is not an array, return `null`.
 * - Ignore non-array pairs or missing values.
 * - If nothing contributed to the sum, return `null`.
 */
export function sumPairValues(entries) {
  if (!Array.isArray(entries)) return null;
  let sum =0;
  let found= false;
  for (const entry of entries) {
    if (!Array.isArray(entry) || entry.length<2) continue;
    const [,value] = entry;

    if (Number.isFinite(value)) {
      sum += value;
      found = true;
    }
  }

  return found? sum:null;
}