import { describe, expect, it } from "vitest";
import { createCounter } from "../src/thisBasicsLab.js";

describe("createCounter", () => {
  it("uses method calls with this", () => {
    const c = createCounter(10);
    expect(c.read()).toBe(10);
    expect(c.inc(5)).toBe(15);
    expect(c.inc()).toBe(16);
  });

  it("ignores bad deltas", () => {
    const c = createCounter(0);
    c.inc(Number.NaN);
    expect(c.read()).toBe(0);
  });
});
