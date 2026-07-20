/**
 * Square a finite number. Non-numbers or non-finite numbers return NaN.
 * Implement as a function declaration (starts with `function square` at top-level in this module).
 */
export function square(n) {
  
  if(typeof n==="number" && Number.isFinite(n)) {
    return n*n;
  }

  return Number.NaN;
}

/**
 * Cube a finite number. Non-numbers or non-finite numbers return NaN.
 * Implement as a `const` binding to a function expression (not an arrow).
 */
export const cube = function (n) {
  if(typeof n==="number" && Number.isFinite(n)) {
    return n*n*n;
  }

  return Number.NaN;
};
