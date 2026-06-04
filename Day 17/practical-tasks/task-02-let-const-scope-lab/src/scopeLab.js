/**
 * Classic `var` loop closure trap: all functions close over the same binding.
 * @returns {number[]}
 */
export function varLoopClosureMappedValues() {
  // TODO(Day17-task02): Implement per TASK_INSTRUCTIONS.md
  return [];
}

/**
 * `let` loop closure: each iteration gets its own binding.
 * @returns {number[]}
 */
export function letLoopClosureMappedValues() {
  // TODO(Day17-task02): Implement per TASK_INSTRUCTIONS.md
  return [];
}

/**
 * Demonstrate block-local shadowing with `let`.
 * @returns {number}
 */
export function blockShadowValue() {
  // TODO(Day17-task02): Implement per TASK_INSTRUCTIONS.md
  return 0;
}

/**
 * `const` prevents rebinding, but object properties may still change.
 * @returns {number}
 */
export function constObjectPropertyMutation() {
  // TODO(Day17-task02): Implement per TASK_INSTRUCTIONS.md
  return 0;
}
