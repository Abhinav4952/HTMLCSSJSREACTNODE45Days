import { describe, expect, it } from "vitest";
import { isThreeDigits } from "../src/classesLab.js";

describe("isThreeDigits", () => {
  it("matches exactly three digits", () => {
    expect(isThreeDigits("909")).toBe(true);
    expect(isThreeDigits("90")).toBe(false);
    expect(isThreeDigits("9090")).toBe(false);
  });
});
