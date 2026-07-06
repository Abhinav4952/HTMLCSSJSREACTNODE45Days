/**
 * Pick a subset of keys from a plain object using dynamic access.
 *
 * Rules:
 * - If `source` is not a plain object, return `null`.
 * - If `keys` is not an array, return `null`.
 * - For each key in `keys` (in order), if `Object.prototype.hasOwnProperty.call(source, key)`, copy `source[key]`.
 * - Ignore keys not present as own properties.
 */

function isPlainObject(x){
  if(x===null) {
    return false;
  }
  let p= Object.getPrototypeOf(x)
  return p===Object.prototype || p===null;
}

export function pickOwn(source, keys) {
  let res={}
  if(isPlainObject(source) && Array.isArray(keys)) {
    for(const key of keys) {
      if(Object.prototype.hasOwnProperty.call(source,key)) {
        res[key]=source[key];
      }
    }
    return res;
  }
  return null;
}

/**
 * Build an object from entries like `[["a", 1], ["b", 2]]`.
 *
 * Rules:
 * - If `entries` is not an array, return `null`.
 * - Ignore non-array rows.
 * - For each row `[k, v]` where `k` is a non-empty string, set `out[k] = v` (later duplicates win).
 */
export function objectFromEntries(entries) {
  if(Array.isArray(entries)) {
    let res = {};
    for(const pair of entries) {
      if(!Array.isArray(pair)) continue;
      let k = pair[0],v=pair[1]
      if(typeof k==="string" && k.length>0) {
        res[k] = v
      }
    }
    return res;
  }
  return null;
}
