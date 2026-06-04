import { describe, expect, it } from "vitest";
import { productOfNumericValues, sumPairValues } from "../src/forOfLab.js";

describe("productOfNumericValues", () => {
  it("multiplies finite numbers", () => {
    expect(productOfNumericValues({ a: 2, b: 3, c: "x" })).toBe(6);
  });

  it("returns null when nothing numeric", () => {
    expect(productOfNumericValues({ a: "nope" })).toBeNull();
  });

  it("rejects non-objects", () => {
    expect(productOfNumericValues(undefined)).toBeNull();
  });
});

describe("sumPairValues", () => {
  it("sums using for..of traversal", () => {
    expect(
      sumPairValues([
        ["a", 1],
        ["b", 2],
        ["c", "x"],
      ]),
    ).toBe(3);
  });

  it("returns null for empty contributions", () => {
    expect(sumPairValues([["a", Number.NaN]])).toBeNull();
  });
});
