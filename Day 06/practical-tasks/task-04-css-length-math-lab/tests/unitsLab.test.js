import { describe, expect, it } from "vitest";
import {
  clampNumber,
  nestedEmFontPx,
  parsePx,
  parseRem,
  remToPx,
  vwContributionPx,
} from "../src/unitsLab.js";

describe("clampNumber", () => {
  it("returns value when inside range", () => {
    expect(clampNumber(3, 0, 5)).toBe(3);
  });

  it("clamps high", () => {
    expect(clampNumber(10, 0, 5)).toBe(5);
  });

  it("clamps low", () => {
    expect(clampNumber(-1, 0, 5)).toBe(0);
  });

  it("allows touching bounds", () => {
    expect(clampNumber(0, 0, 5)).toBe(0);
    expect(clampNumber(5, 0, 5)).toBe(5);
  });

  it("throws RangeError when max < min", () => {
    expect(() => clampNumber(1, 5, 4)).toThrow(RangeError);
    expect(() => clampNumber(1, 5, 4)).toThrow("max < min");
  });

  it("returns NaN if any arg is NaN", () => {
    expect(clampNumber(NaN, 0, 1)).toBeNaN();
    expect(clampNumber(1, NaN, 2)).toBeNaN();
    expect(clampNumber(1, 0, NaN)).toBeNaN();
  });
});

describe("parsePx", () => {
  it("parses integers and decimals", () => {
    expect(parsePx("12px")).toBe(12);
    expect(parsePx(" 12.5px ")).toBe(12.5);
});

  it("returns null for invalid strings", () => {
    expect(parsePx("12")).toBeNull();
    expect(parsePx("px")).toBeNull();
    expect(parsePx("12em")).toBeNull();
    expect(parsePx("")).toBeNull();
    expect(parsePx("   ")).toBeNull();
  });

  it("returns null for non-strings", () => {
    expect(parsePx(null)).toBeNull();
    expect(parsePx(12)).toBeNull();
  });
});

describe("parseRem", () => {
  it("parses rem factors", () => {
    expect(parseRem("1.25rem")).toBe(1.25);
    expect(parseRem("2rem")).toBe(2);
    expect(parseRem(" 0.875rem ")).toBe(0.875);
  });

  it("returns null for invalid strings", () => {
    expect(parseRem("1.25")).toBeNull();
    expect(parseRem("rem")).toBeNull();
    expect(parseRem("10px")).toBeNull();
  });
});

describe("remToPx", () => {
  it("converts rem to px", () => {
    expect(remToPx(1.25, 16)).toBe(20);
  });

  it("defaults root to 16", () => {
    expect(remToPx(1)).toBe(16);
  });

  it("returns NaN for invalid inputs", () => {
    expect(remToPx(Number.POSITIVE_INFINITY, 16)).toBeNaN();
    expect(remToPx(1, 0)).toBeNaN();
    expect(remToPx(1, -16)).toBeNaN();
    expect(remToPx(1, NaN)).toBeNaN();
  });
});

describe("nestedEmFontPx", () => {
  it("returns rootPx for empty factors", () => {
    expect(nestedEmFontPx([], 16)).toBe(16);
  });

  it("multiplies factors", () => {
    expect(nestedEmFontPx([1.25, 0.8], 16)).toBeCloseTo(16 * 1.25 * 0.8);
  });

  it("returns NaN for invalid factors or root", () => {
    expect(nestedEmFontPx([1, -1], 16)).toBeNaN();
    expect(nestedEmFontPx([1, Number.NaN], 16)).toBeNaN();
    expect(nestedEmFontPx([1], 0)).toBeNaN();
  });
});

describe("vwContributionPx", () => {
  it("computes vw contribution", () => {
    expect(vwContributionPx(10, 800)).toBe(80);
    expect(vwContributionPx(0, 1234)).toBe(0);
  });

  it("returns NaN for invalid viewport width", () => {
    expect(vwContributionPx(10, -1)).toBeNaN();
    expect(vwContributionPx(10, NaN)).toBeNaN();
  });

  it("returns NaN for invalid vw", () => {
    expect(vwContributionPx(NaN, 800)).toBeNaN();
  });
});


