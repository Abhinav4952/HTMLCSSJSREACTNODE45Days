/**
 * Parse `"12%"` / `" 3.5 % "` into a **fraction** (`0.12`, `0.035`).
 * - Return `null` if the string does not match `%` suffix pattern after trim.
 * - Reject `Infinity` / `NaN` results.
 */
export function parsePercentToFraction(input) {
  input = input.trim();
  if(input.endsWith("%")) {
    let parts = input.split("%");
    if(parts.length===2 && parts[1]==="") var [res,]=parts;
    if(Number.isFinite(Number(res))) return Number(res)/100;
  }
  return null;
}

/**
 * Merge two count maps (objects with **finite numeric** values) by summing overlapping keys.
 * - Non-finite numbers and non-numbers should be ignored for that key.
 * - Return a **new** plain object; do not mutate inputs.
 */
export function mergeCountObjects(left, right) {
  let res = {}
  for(const [key,value] of Object.entries(left)) {
    if(typeof value==="number" && Number.isFinite(value))
      res[key] = value;
  }
  for(const [key,value] of Object.entries(right)) {
    if(typeof value==="number" && Number.isFinite(value))
      res[key] = (res[key] || 0) + value;
  }
  return res;
}
