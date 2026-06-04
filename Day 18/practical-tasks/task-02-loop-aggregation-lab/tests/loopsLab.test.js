import { describe, expect, it } from "vitest";
import { sumPrefixUntilCap } from "../src/loopsLab.js";

describe("sumPrefixUntilCap", () => {
  it("sums a prefix under cap", () => {
    expect(sumPrefixUntilCap([10, 20, 30], 25)).toBe(10);
    expect(sumPrefixUntilCap([1, 2, 3, 4], 6)).toBe(6); // 1+2+3
  });

  it("returns 0 when cap is invalid", () => {
    expect(sumPrefixUntilCap([1, 2, 3], Number.NaN)).toBe(0);
    expect(sumPrefixUntilCap([1, 2, 3], Number.POSITIVE_INFINITY)).toBe(0);
  });

  it("returns 0 when nums is not an array", () => {
    expect(sumPrefixUntilCap(null, 10)).toBe(0);
  });

  it("stops before exceeding cap", () => {
    expect(sumPrefixUntilCap([5, 5, 5], 10)).toBe(10);
  });

  it("stops on invalid elements", () => {
    expect(sumPrefixUntilCap([1, 2, "x", 99], 1000)).toBe(3);
    expect(sumPrefixUntilCap([1, 2, Number.NaN, 3], 1000)).toBe(3);
  });
});
