import { L } from "vitest/dist/chunks/reporters.nr4dxCkA.js";

export function clampNumber(value, min, max) {
  // TODO(Day06-task04): Implement clampNumber per TASK_INSTRUCTIONS.md
  if(Number.isNaN(min) || Number.isNaN(value) || Number.isNaN(max)) {
    return NaN;
  } else if(min>max) {
    throw new RangeError("max < min")
  } else {
    if(value<min) return min;
    else if(value>max) return max;
    else if(value>=min && value<=max) return value;
  }
  
  return 0;
}

export function parsePx(input) {
  // TODO(Day06-task04): Implement parsePx per TASK_INSTRUCTIONS.md

  if(typeof input!="string") return null;
  input = input.trim()
  if(input.length==0) return null;
  else if(!input.endsWith("px")) return null;

  if(Number.isNaN(Number(input.slice(0,-2)))) return null;
  console.log("Slice value : ",input.slice(-2));
  return Number(input.slice(0,-2));
}

export function parseRem(input) {
  
  // TODO(Day06-task04): Implement parseRem per TASK_INSTRUCTIONS.md

  if(typeof input!="string") return null;
  input = input.trim()
  if(input.length==0) return null;
  else if(!input.endsWith("rem")) return null;
  else if(Number.isNaN(Number(input.slice(0,-3)))) return null;

  return Number(input.slice(0,-3));
}

export function remToPx(rem, rootPx = 16) {
  // TODO(Day06-task04): Implement remToPx per TASK_INSTRUCTIONS.md
  if(!Number.isFinite(rem) || !Number.isFinite(rootPx)) return NaN;
  else if(rootPx<=0) return NaN;

  return rem*rootPx;
}

function product(arr) {
  let pro = 0;

  for(let i of arr) {
    prod *= i;
  }
  return prod;
}

export function nestedEmFontPx(emFactors, rootPx = 16) {
  // TODO(Day06-task04): Implement nestedEmFontPx per TASK_INSTRUCTIONS.md

  if(!Number.isFinite(rootPx) || rootPx<=0) return NaN;
  else if(emFactors.length == 0) return rootPx;
  else {
    for(let i of emFactors) {
      if(Number.isNaN(i) || !Number.isFinite(i) || i<=0) return NaN;
    }
  }

  return rootPx*product(emFactors);
}

export function vwContributionPx(vw, viewportWidthPx) {
  // TODO(Day06-task04): Implement vwContributionPx per TASK_INSTRUCTIONS.md

  if(!Number.isFinite(vw) || !Number.isFinite(viewportWidthPx) || viewportWidthPx<0) return NaN;

  return vw * viewportWidthPx / 100;
}

console.log(parsePx("12"))
console.log(parsePx("px"))
console.log(parsePx("em"))
console.log(parsePx("12em"))
console.log(parsePx(""))
console.log(parsePx("   "))