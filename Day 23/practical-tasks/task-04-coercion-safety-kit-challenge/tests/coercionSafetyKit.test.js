import { describe, expect, it } from "vitest";
import { mergeCountObjects, parsePercentToFraction } from "../src/coercionSafetyKit.js";

describe("parsePercentToFraction", () => {
  it("parses percent strings to fractions", () => {
    expect(parsePercentToFraction("12%")).toBeCloseTo(0.12);
    expect(parsePercentToFraction(" 3.5 % ")).toBeCloseTo(0.035);
  });

  it("rejects invalid patterns", () => {
    expect(parsePercentToFraction("12")).toBeNull();
    expect(parsePercentToFraction("12%%")).toBeNull();
  });
});

describe("mergeCountObjects", () => {
  it("sums overlapping numeric keys immutably", () => {
    const a = { x: 1, y: 2 };
    const b = { y: 3, z: 4 };
    const merged = mergeCountObjects(a, b);
    expect(merged).toEqual({ x: 1, y: 5, z: 4 });
    expect(a).toEqual({ x: 1, y: 2 });
  });

  it("ignores junk values", () => {
    expect(
      mergeCountObjects({ a: 1, b: "2" }, { b: 3, c: Number.NaN }),
    ).toEqual({ a: 1, b: 3 });
  });
});
