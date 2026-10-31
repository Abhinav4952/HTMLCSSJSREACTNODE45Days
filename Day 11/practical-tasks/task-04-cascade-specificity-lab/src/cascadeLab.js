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
  if (typeof selector !== "string" || selector.length === 0) {
    return null;
  }
  // Initialize specificity parts
  let ids = 0;
  let classes = 0;
  let types = 0;

  // Check if the selector starts with a type selector
  const typeMatch = selector.match(/^[a-z]+/);
  if (typeMatch) {
    types = 1;
    selector = selector.slice(typeMatch[0].length);
  }

  // Count IDs and classes
  ids = (selector.match(/#/g) || []).length;
  classes = (selector.match(/\./g) || []).length;

  return { ids, classes, types };
}

/**
 * Compare two { ids, classes, types } records using the classic tuple ordering.
 * @returns {1|-1|0} 1 if a wins, -1 if b wins, 0 on tie
 */
export function compareSpecificityParts(a, b) {
  // TODO(Day11-task04): Implement compareSpecificityParts per TASK_INSTRUCTIONS.md
  if (a.ids !== b.ids) {
    return a.ids > b.ids ? 1 : -1;
  }
  if (a.classes !== b.classes) {
    return a.classes > b.classes ? 1 : -1;
  }
  if (a.types !== b.types) {
    return a.types > b.types ? 1 : -1;
  }
  return 0;
}

/**
 * CSS opacity multiplies down the tree. Model that as simple multiplication.
 * Return NaN unless both inputs are finite numbers in the inclusive range [0, 1].
 */
export function effectiveNestedOpacity(parentOpacity, childOpacity) {
  // TODO(Day11-task04): Implement effectiveNestedOpacity per TASK_INSTRUCTIONS.md
  if (typeof parentOpacity === "number" && typeof childOpacity === "number" &&
      isFinite(parentOpacity) && isFinite(childOpacity) &&
      parentOpacity >= 0 && parentOpacity <= 1 &&
      childOpacity >= 0 && childOpacity <= 1) {
    return parentOpacity * childOpacity;
  }
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
  if (!Array.isArray(bottomRgb) || !Array.isArray(topRgb) ||
      bottomRgb.length !== 3 || topRgb.length !== 3 ||
      !bottomRgb.every(c => Number.isInteger(c) && c >= 0 && c <= 255) ||
      !topRgb.every(c => Number.isInteger(c) && c >= 0 && c <= 255) ||
      typeof topAlpha !== "number" || !isFinite(topAlpha) || topAlpha < 0 || topAlpha > 1) {
    return null;
  }

  const [bottomR, bottomG, bottomB] = bottomRgb;
  const [topR, topG, topB] = topRgb;

  const blendedR = Math.round((1 - topAlpha) * bottomR + topAlpha * topR);
  const blendedG = Math.round((1 - topAlpha) * bottomG + topAlpha * topG);
  const blendedB = Math.round((1 - topAlpha) * bottomB + topAlpha * topB);

  return [blendedR, blendedG, blendedB];
}
