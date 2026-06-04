import { describe, expect, it } from "vitest";
import { StepCounter } from "../src/counterClass.js";

describe("StepCounter", () => {
  it("uses instance fields", () => {
    const c = new StepCounter(2);
    expect(c.tick()).toBe(2);
    expect(c.tick(2)).toBe(6);
  });

  it("ignores invalid constructor step", () => {
    const c = new StepCounter(-1);
    expect(c.step).toBe(1);
  });
});
