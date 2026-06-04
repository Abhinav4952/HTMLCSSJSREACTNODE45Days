import { describe, expect, it } from "vitest";
import { createCachedNumericSum } from "../src/memoChallenge.js";

describe("createCachedNumericSum", () => {
  it("sums numeric properties", () => {
    const m = createCachedNumericSum();
    expect(m.sum({ a: 1, b: 2, c: "x" })).toBe(3);
  });

  it("treats key-order permutations as the same cache key", () => {
    const m = createCachedNumericSum();
    expect(m.sum({ a: 1, b: 2 })).toBe(3);
    expect(m.sum({ b: 2, a: 1 })).toBe(3);
    expect(m.misses()).toBe(1);
  });

  it("rejects non-plain objects", () => {
    const m = createCachedNumericSum();
    expect(m.sum([])).toBeNull();
  });
});
