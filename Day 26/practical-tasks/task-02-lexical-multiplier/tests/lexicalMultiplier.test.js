import { describe, expect, it } from "vitest";
import { makeMultiplier } from "../src/lexicalMultiplier.js";

describe("makeMultiplier", () => {
  it("closes over scale", () => {
    const triple = makeMultiplier(3);
    expect(triple(4)).toBe(12);
  });

  it("creates independent functions", () => {
    expect(makeMultiplier(2)(5)).toBe(10);
    expect(makeMultiplier(0.5)(8)).toBe(4);
  });

  it("handles invalid scale", () => {
    const bad = makeMultiplier(Number.NaN);
    expect(Number.isNaN(bad(1))).toBe(true);
  });
});
