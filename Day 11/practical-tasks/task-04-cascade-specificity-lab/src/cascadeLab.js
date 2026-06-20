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

  if(!selector || typeof selector!=="string" || selector.trim().length===0 ) return null;
  else if(/^(?:[a-z]+|[\.#][a-z]+)*$/.test(selector)){
    let i = 0;
    let res = {ids : 0,classes: 0, types : 0}
    while(i<selector.length) {
      if(i==0 && (selector[i]!=='.' && selector[i]!=='#')) {
        while(i<selector.length && selector[i]!=='.' && selector[i]!=='#') {
          i++;
        } 
        res.types++;
      } else if(selector[i]==='.') {
        i++;
        while(i<selector.length && selector[i]!=='.' && selector[i]!=='#') {
          i++;
        } 
        res.classes++;
      } else {
        i++;
          while(i<selector.length && selector[i]!=='.' && selector[i]!=='#') {
            i++;
          } 
          res.ids++;
      }
    }
    return res;
  }
  return null;
}

/**
 * Compare two { ids, classes, types } records using the classic tuple ordering.
 * @returns {1|-1|0} 1 if a wins, -1 if b wins, 0 on tie
 */
export function compareSpecificityParts(a, b) {
  // TODO(Day11-task04): Implement compareSpecificityParts per TASK_INSTRUCTIONS.md
  if(a.ids>b.ids) return 1;
  else if(a.ids<b.ids) return -1;
  else if(a.classes>b.classes) return 1;
  else if(a.classes<b.classes) return -1;
  else if(a.types>b.types) return 1;
  else if(a.types<b.types) return -1;
  
  return 0;
}

/**
 * CSS opacity multiplies down the tree. Model that as simple multiplication.
 * Return NaN unless both inputs are finite numbers in the inclusive range [0, 1].
 */
export function effectiveNestedOpacity(parentOpacity, childOpacity) {
  // TODO(Day11-task04): Implement effectiveNestedOpacity per TASK_INSTRUCTIONS.md
  if (parentOpacity < 0 || childOpacity < 0 || parentOpacity > 1 || childOpacity > 1) return NaN;
  return parentOpacity * childOpacity;
}

/**
 * Alpha blend solid `topRgb` over solid `bottomRgb`.
 * Each rgb is an array of 3 integers in [0, 255].
 * `topAlpha` must be finite in [0, 1].
 * Return an array `[r,g,b]` of integers rounded to nearest, clamped to [0,255].
 * Return NaN (as a number) if inputs are invalid? Tests will specify: use null for invalid.
 */
export function blendRgbOver(bottomRgb, topRgb, topAlpha) {

  if (!Array.isArray(bottomRgb) || !Array.isArray(topRgb) || bottomRgb.length !== 3 || topRgb.length !== 3) {
    return null;
  }

  for (const channel of [...bottomRgb, ...topRgb]) {
    if (!Number.isInteger(channel) || channel < 0 || channel > 255) {
      return null;
    }
  }

  if (
    !Number.isFinite(topAlpha) || topAlpha < 0 || topAlpha > 1) {
    return null;
  }

  return bottomRgb.map((bottom, i) => {
    const top=topRgb[i];
    const blended=Math.round( top*topAlpha + bottom*(1 - topAlpha));

    return Math.max(0, Math.min(255, blended));
  });
}

console.log(
  "Test 1:",
  blendRgbOver([0, 0, 0], [255, 255, 255], 0.5),
  "Expected:",
  [128, 128, 128]
);

console.log(
  "Test 2:",
  blendRgbOver([0, 0, 255], [255, 0, 0], 0.3333333333),
  "Expected:",
  [85, 0, 170]
);

console.log(
  "Test 3:",
  blendRgbOver([1, 2, 3], [9, 8, 7], 0),
  "Expected:",
  [1, 2, 3]
);

console.log(
  "Test 4:",
  blendRgbOver([1, 2, 3], [9, 8, 7], 1),
  "Expected:",
  [9, 8, 7]
);

console.log(
  "Test 5:",
  blendRgbOver(null, [0, 0, 0], 0.5),
  "Expected:",
  null
);

console.log(
  "Test 6:",
  blendRgbOver([0, 0], [0, 0, 0], 0.5),
  "Expected:",
  null
);

console.log(
  "Test 7:",
  blendRgbOver([0, 0, 0], [0, 0, 0], 1.01),
  "Expected:",
  null
);

console.log(
  "Test 8:",
  blendRgbOver([0, 0, 0], [0, 0, 0], -0.01),
  "Expected:",
  null
);

console.log(
  "Test 9:",
  blendRgbOver([0, 0, NaN], [0, 0, 0], 0.5),
  "Expected:",
  null
);

console.log(
  "Test 10:",
  blendRgbOver([0.5, 0, 0], [0, 0, 0], 0.5),
  "Expected:",
  null
);