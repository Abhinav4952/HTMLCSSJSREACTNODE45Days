import { describe, expect, it } from "vitest";
import { classifyEquality } from "../src/equalityLab.js";

describe("classifyEquality", () => {
  it("detects SameValue for NaN", () => {
    expect(classifyEquality(Number.NaN, Number.NaN)).toBe("same-value");
  });

  it("distinguishes signed zero under strict vs SameValue", () => {
    expect(classifyEquality(0, -0)).toBe("strict");
    expect(classifyEquality(-0, 0)).toBe("strict");
  });

  it("detects loose-only equality", () => {
    expect(classifyEquality(0, false)).toBe("loose");
    expect(classifyEquality(null, undefined)).toBe("loose");
  });

  it("marks genuinely different values", () => {
    expect(classifyEquality(1, 2)).toBe("different");
  });
});
