import { describe, expect, it, vi } from "vitest";
import {
  createTimeoutHarness,
  letBindingThrowsInTdz,
  varBindingBeforeInit,
} from "../src/hoistingTdzChallenge.js";

describe("varBindingBeforeInit", () => {
  it("demonstrates var hoisting read before init", () => {
    expect(varBindingBeforeInit()).toEqual(["undefined", undefined]);
  });
});

describe("letBindingThrowsInTdz", () => {
  it("detects TDZ ReferenceError", () => {
    expect(letBindingThrowsInTdz()).toBe(true);
  });
});

describe("createTimeoutHarness", () => {
  it("schedules without running fn immediately", () => {
    vi.useFakeTimers();
    const fn = vi.fn();
    const harness = createTimeoutHarness(fn, 10);
    harness.schedule();
    expect(fn).not.toHaveBeenCalled();
    harness.flush();
    expect(fn).toHaveBeenCalledTimes(1);
    vi.useRealTimers();
  });

  it("uses default ms = 0 binding in signature", () => {
    const fn = vi.fn();
    const harness = createTimeoutHarness(fn);
    expect(typeof harness.schedule).toBe("function");
    expect(typeof harness.flush).toBe("function");
  });
});
