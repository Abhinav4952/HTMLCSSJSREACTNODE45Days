import { describe, expect, it } from "vitest";
import { isLexicographicGreater, isNumericGreater } from "../src/relationalLab.js";

describe("isLexicographicGreater", () => {
  it("compares digit strings lexicographically", () => {
    expect(isLexicographicGreater("2", "12")).toBe(true);
    expect(isLexicographicGreater("12", "2")).toBe(false);
  });

  it("rejects non-strings", () => {
    expect(isLexicographicGreater("1", 2)).toBeNull();
  });
});

describe("isNumericGreater", () => {
  it("compares digit strings numerically", () => {
    expect(isNumericGreater("2", "12")).toBe(false);
    expect(isNumericGreater("12", "2")).toBe(true);
  });

  it("returns null when not finite numbers", () => {
    expect(isNumericGreater("x", "1")).toBeNull();
  });
});
