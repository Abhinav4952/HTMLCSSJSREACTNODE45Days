/**
 * Shallow-merge two plain objects. Later keys win.
 *
 * Rules:
 * - If `a` or `b` is not a plain object, return `null`.
 * - "Plain object" means: not null and `Object.getPrototypeOf(x)` is `Object.prototype` or `null`.
 */

function isPlainObject(x){
  if(x===null) return false;
  let p= Object.getPrototypeOf(x)
  return p===Object.prototype || p===null;
}

export function shallowMergeRecords(a, b) {
  
  if(isPlainObject(a) && isPlainObject(b)) {
    return {...a,...b}
  }
  return null;
}


