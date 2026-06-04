import { describe, expect, it } from "vitest";
import { mapWith, negate } from "../src/callbackLab.js";

describe("mapWith", () => {
  it("maps with index", () => {
    expect(mapWith([10, 20], (v, i) => v + i)).toEqual([10, 21]);
  });

  it("rejects non-arrays", () => {
    expect(mapWith({ length: 1 }, () => 1)).toBeNull();
  });
});

describe("negate", () => {
  it("wraps a predicate", () => {
    const isEven = (n) => n % 2 === 0;
    const isOdd = negate(isEven);
    expect(isOdd(3)).toBe(true);
    expect(isOdd(2)).toBe(false);
  });
});
