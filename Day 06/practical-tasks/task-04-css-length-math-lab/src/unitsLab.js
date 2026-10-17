export function clampNumber(value, min, max) {
  // TODO(Day06-task04): Implement clampNumber per TASK_INSTRUCTIONS.md
  const clampedValue = Math.max(min, Math.min(value, max));
  return clampedValue;
}

export function parsePx(input) {
  // TODO(Day06-task04): Implement parsePx per TASK_INSTRUCTIONS.md
  return parseFloat(input);
}

export function parseRem(input) {
  // TODO(Day06-task04): Implement parseRem per TASK_INSTRUCTIONS.md
  return parseFloat(input);
}

export function remToPx(rem, rootPx = 16) {
  // TODO(Day06-task04): Implement remToPx per TASK_INSTRUCTIONS.md
  return rem * rootPx;
}

export function nestedEmFontPx(emFactors, rootPx = 16) {
  // TODO(Day06-task04): Implement nestedEmFontPx per TASK_INSTRUCTIONS.md
  nestedEmFactors = emFactors.reduce((acc, factor) => acc * factor, 1);
  return nestedEmFactors * rootPx;
}

export function vwContributionPx(vw, viewportWidthPx) {
  // TODO(Day06-task04): Implement vwContributionPx per TASK_INSTRUCTIONS.md
  return vw * viewportWidthPx / 100;
}
