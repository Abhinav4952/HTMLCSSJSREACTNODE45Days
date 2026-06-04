/**
 * Parse a simplified compound selector used only for this lab:
 * - Optional single type selector at the start: lowercase `[a-z]+`
 * - Then zero or more `#id` or `.class` tokens concatenated without spaces.
 * - No combinators, pseudo-classes, attributes, or uppercase tags.
 *
 * Examples:
 * - "div" -> { ids: 0, classes: 0, types: 1 }
 * - ".btn.primary" -> { ids: 0, classes: 2, types: 0 }
 * - "article#hero.lede" -> { ids: 1, classes: 1, types: 1 }
 */
export function compoundSpecificityParts(selector) {
  // TODO(Day11-task04): Implement compoundSpecificityParts per TASK_INSTRUCTIONS.md
  return null;
}

/**
 * Compare two { ids, classes, types } records using the classic tuple ordering.
 * @returns {1|-1|0} 1 if a wins, -1 if b wins, 0 on tie
 */
export function compareSpecificityParts(a, b) {
  // TODO(Day11-task04): Implement compareSpecificityParts per TASK_INSTRUCTIONS.md
  return 0;
}

/**
 * CSS opacity multiplies down the tree. Model that as simple multiplication.
 * Return NaN unless both inputs are finite numbers in the inclusive range [0, 1].
 */
export function effectiveNestedOpacity(parentOpacity, childOpacity) {
  // TODO(Day11-task04): Implement effectiveNestedOpacity per TASK_INSTRUCTIONS.md
  return NaN;
}

/**
 * Alpha blend solid `topRgb` over solid `bottomRgb`.
 * Each rgb is an array of 3 integers in [0, 255].
 * `topAlpha` must be finite in [0, 1].
 * Return an array `[r,g,b]` of integers rounded to nearest, clamped to [0,255].
 * Return NaN (as a number) if inputs are invalid? Tests will specify: use null for invalid.
 */
export function blendRgbOver(bottomRgb, topRgb, topAlpha) {
  // TODO(Day11-task04): Implement blendRgbOver per TASK_INSTRUCTIONS.md
  return null;
}
