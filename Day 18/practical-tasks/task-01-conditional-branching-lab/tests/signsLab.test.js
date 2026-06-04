import { describe, expect, it } from "vitest";
import { signCategory } from "../src/signsLab.js";

describe("signCategory", () => {
  it("classifies sign for finite numbers", () => {
    expect(signCategory(3)).toBe("positive");
    expect(signCategory(-1)).toBe("negative");
    expect(signCategory(0)).toBe("zero");
    expect(signCategory(-0)).toBe("zero");
  });

  it("handles NaN and infinities", () => {
    expect(signCategory(Number.NaN)).toBe("nan");
    expect(signCategory(Number.POSITIVE_INFINITY)).toBe("other");
    expect(signCategory(Number.NEGATIVE_INFINITY)).toBe("other");
  });

  it("rejects non-numbers", () => {
    expect(signCategory("3")).toBe("other");
    expect(signCategory(null)).toBe("other");
    expect(signCategory(undefined)).toBe("other");
    expect(signCategory({ valueOf: () => 1 })).toBe("other");
  });
});
