import { describe, expect, it } from "vitest";
import { createCounter } from "../src/methodsLab.js";

describe("createCounter", () => {
  it("starts at a finite number or 0", () => {
    expect(createCounter(3).read()).toBe(3);
    expect(createCounter(Number.NaN).read()).toBe(0);
  });

  it("adds with default step", () => {
    const c = createCounter(1);
    c.add();
    c.add(2);
    expect(c.read()).toBe(4);
  });

  it("resets with validation", () => {
    const c = createCounter(10);
    c.reset(2);
    expect(c.read()).toBe(2);
    c.reset(Number.POSITIVE_INFINITY);
    expect(c.read()).toBe(0);
  });
});
