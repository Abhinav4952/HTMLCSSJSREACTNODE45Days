/**
 * Curry any binary function `fn(a, b)` into `curryBinary(fn)(a)(b)`.
 */
export function curryBinary(fn) {
  return (a) => (b) => fn(a,b);
}

/**
 * Return a clamp function `clamp(lo)(hi)(value)` enforcing `lo <= value <= hi`.
 * Keep the **curried call shape** from tests (`makeClamp(0)(10)(value)`).
 */
export function makeClamp(lo) {
  return (hi) => (value) => {
    if(value<lo) return lo;
    if(value>hi) return hi;
    return value;
  };
}
