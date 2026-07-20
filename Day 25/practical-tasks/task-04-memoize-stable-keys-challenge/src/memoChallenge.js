/**
 * Create a memoized summer over **plain objects** whose own enumerable values are finite numbers.
 *
 * Requirements:
 * - `sum(cfg)` returns the sum of finite numeric values in `cfg` (ignore non-numbers / non-finite).
 * - If `cfg` is not a plain object (same rule as Day 22: only `{}` literals / `Object.create(null)` in tests), return `null`.
 * - Cache results so logically-equal configs with different **key insertion order** still hit the cache.
 * - Expose `misses()` counting how many times the expensive aggregation ran (cache misses).
 */

function isPlainObject(x){
  if(x===null) return false;
  let p= Object.getPrototypeOf(x)
  return p===Object.prototype || p===null;
}

export function createCachedNumericSum() {
  return {
    res : {},
    sum(cfg) {
      if(isPlainObject(cfg)) {
        let sum=0;
        for(const [key,value] of Object.entries(cfg)) {
          if(typeof value ==="number" && Number.isFinite(value)) sum+=value;
        }
        this.res[cfg]=sum;
        return sum;
      }
      return null;
    },
    misses() {
      return Object.keys(this.res).length;
    },
  };
}
