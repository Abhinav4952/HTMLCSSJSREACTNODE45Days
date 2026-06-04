import { describe, expect, it } from "vitest";
import { firstIndexGreaterThan, tail } from "../src/searchLab.js";

describe("tail", () => {
  it("returns the last n elements", () => {
    expect(tail([1, 2, 3, 4], 2)).toEqual([3, 4]);
    expect(tail([1, 2], 5)).toEqual([1, 2]);
  });

  it("handles edge cases", () => {
    expect(tail([1, 2, 3], 0)).toEqual([]);
  });

  it("rejects invalid args", () => {
    expect(tail(null, 1)).toBeNull();
    expect(tail([1, 2], Number.NaN)).toBeNull();
    expect(tail([1, 2], 1.5)).toBeNull();
    expect(tail([1, 2], -1)).toBeNull();
  });
});

describe("firstIndexGreaterThan", () => {
  it("finds first match", () => {
    expect(firstIndexGreaterThan([1, 5, 3], 4)).toBe(1);
  });

  it("returns -1 when none", () => {
    expect(firstIndexGreaterThan([1, 2, 3], 9)).toBe(-1);
  });

  it("ignores non-finite elements", () => {
    expect(firstIndexGreaterThan([1, Number.NaN, 10], 5)).toBe(2);
  });

  it("rejects invalid args", () => {
    expect(firstIndexGreaterThan(null, 1)).toBeNull();
    expect(firstIndexGreaterThan([1], Number.POSITIVE_INFINITY)).toBeNull();
  });
});
