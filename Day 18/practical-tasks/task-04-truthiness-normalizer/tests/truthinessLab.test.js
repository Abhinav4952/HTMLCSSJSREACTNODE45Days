import { describe, expect, it } from "vitest";
import { triClassifyBooleaniness } from "../src/truthinessLab.js";

describe("triClassifyBooleaniness", () => {
  it("detects strict booleans", () => {
    expect(triClassifyBooleaniness(true)).toBe("strict-true");
    expect(triClassifyBooleaniness(false)).toBe("strict-false");
  });

  it("classifies truthy non-booleans", () => {
    expect(triClassifyBooleaniness(1)).toBe("truthy");
    expect(triClassifyBooleaniness("x")).toBe("truthy");
    expect(triClassifyBooleaniness([])).toBe("truthy");
  });

  it("classifies falsy non-booleans", () => {
    expect(triClassifyBooleaniness(0)).toBe("falsy");
    expect(triClassifyBooleaniness("")).toBe("falsy");
    expect(triClassifyBooleaniness(null)).toBe("falsy");
    expect(triClassifyBooleaniness(undefined)).toBe("falsy");
    expect(triClassifyBooleaniness(Number.NaN)).toBe("falsy");
  });
});
