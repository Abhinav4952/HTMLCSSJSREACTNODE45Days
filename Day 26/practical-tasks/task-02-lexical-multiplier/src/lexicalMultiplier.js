/**
 * Return `(x) => x * scale` where `scale` is captured from the outer call.
 * - If `scale` is not a finite number, return a function that always returns `NaN`.
 */
export function makeMultiplier(scale) {

  if(Number.isFinite(scale)) {
    return (x) => x*scale;
  }

  return () => Number.NaN;
}
