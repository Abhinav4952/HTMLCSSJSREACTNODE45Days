import { describe, expect, it } from "vitest";
import { createCounter } from "../src/counterFactory.js";

describe("createCounter", () => {
  it("tracks increments with private state", () => {
    const c = createCounter(10);
    expect(c.read()).toBe(10);
    expect(c.inc()).toBe(11);
    expect(c.inc(4)).toBe(15);
  });

  it("ignores bad deltas", () => {
    const c = createCounter(0);
    c.inc(Number.NaN);
    expect(c.read()).toBe(0);
  });

  it("resets to initial", () => {
    const c = createCounter(5);
    c.inc(10);
    c.reset();
    expect(c.read()).toBe(5);
  });

  it("creates independent counters", () => {
    const a = createCounter(1);
    const b = createCounter(2);
    a.inc();
    expect(a.read()).toBe(2);
    expect(b.read()).toBe(2);
  });
});
