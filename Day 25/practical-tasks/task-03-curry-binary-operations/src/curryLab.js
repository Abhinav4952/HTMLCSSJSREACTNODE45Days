/**
 * Curry any binary function `fn(a, b)` into `curryBinary(fn)(a)(b)`.
 */
export function curryBinary(fn) {
  // TODO(Day25-task03): Implement per TASK_INSTRUCTIONS.md
  return () => () => null;
}

/**
 * Return a clamp function `clamp(lo)(hi)(value)` enforcing `lo <= value <= hi`.
 * Keep the **curried call shape** from tests (`makeClamp(0)(10)(value)`).
 */
export function makeClamp(lo) {
  // TODO(Day25-task03): Implement per TASK_INSTRUCTIONS.md
  return () => () => null;
}
