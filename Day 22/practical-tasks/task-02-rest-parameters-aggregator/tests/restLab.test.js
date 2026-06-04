import { describe, expect, it } from "vitest";
import { firstAndRestSum, maxFinite } from "../src/restLab.js";

describe("firstAndRestSum", () => {
  it("sums finite rest args", () => {
    expect(firstAndRestSum(10, 1, 2, 3)).toEqual({ first: 10, restSum: 6 });
  });

  it("ignores junk in rest", () => {
    expect(firstAndRestSum(0, "x", Number.NaN, 4)).toEqual({ first: 0, restSum: 4 });
  });

  it("rejects invalid first", () => {
    expect(firstAndRestSum("nope", 1)).toBeNull();
  });
});

describe("maxFinite", () => {
  it("uses Math.max with spread", () => {
    expect(maxFinite(3, 9, -2)).toBe(9);
  });

  it("returns NaN when nothing usable", () => {
    expect(Number.isNaN(maxFinite())).toBe(true);
  });
});
