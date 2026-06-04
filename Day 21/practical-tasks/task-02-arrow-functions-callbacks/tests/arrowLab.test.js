import { describe, expect, it } from "vitest";
import { makeScaledAdder, sumPairs } from "../src/arrowLab.js";

describe("sumPairs", () => {
  it("sums finite pairs", () => {
    expect(sumPairs([[1, 2], [3, 4]])).toEqual([3, 7]);
  });

  it("treats invalid parts as 0", () => {
    expect(
      sumPairs([
        [1, "2"],
        [Number.NaN, 2],
        [3],
      ]),
    ).toEqual([1, 2, 3]);
  });

  it("rejects non-array input", () => {
    expect(sumPairs(null)).toBeNull();
  });
});

describe("makeScaledAdder", () => {
  it("returns an adder function", () => {
    const add5 = makeScaledAdder(5);
    expect(add5(10)).toBe(15);
  });

  it("returns NaN for non-finite x", () => {
    const add1 = makeScaledAdder(1);
    expect(Number.isNaN(add1(Number.NaN))).toBe(true);
  });
});
