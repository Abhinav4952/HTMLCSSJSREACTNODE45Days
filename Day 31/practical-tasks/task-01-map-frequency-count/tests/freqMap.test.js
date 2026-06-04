import { describe, expect, it } from "vitest";
import { countTokens } from "../src/freqMap.js";

describe("countTokens", () => {
  it("counts with Map", () => {
    const m = countTokens(["A", "a", "b", ""]);
    expect(m.get("a")).toBe(2);
    expect(m.get("b")).toBe(1);
  });
});
