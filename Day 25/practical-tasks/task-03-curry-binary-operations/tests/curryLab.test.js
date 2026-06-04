import { describe, expect, it } from "vitest";
import { curryBinary, makeClamp } from "../src/curryLab.js";

describe("curryBinary", () => {
  it("curries a binary op", () => {
    const add = (a, b) => a + b;
    expect(curryBinary(add)(2)(3)).toBe(5);
  });
});

describe("makeClamp", () => {
  it("returns nested clampers", () => {
    const clamp0to10 = makeClamp(0)(10);
    expect(clamp0to10(-5)).toBe(0);
    expect(clamp0to10(7)).toBe(7);
    expect(clamp0to10(99)).toBe(10);
  });
});
