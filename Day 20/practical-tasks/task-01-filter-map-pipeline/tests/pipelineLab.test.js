import { describe, expect, it } from "vitest";
import { doublePositives } from "../src/pipelineLab.js";

describe("doublePositives", () => {
  it("filters and maps", () => {
    expect(doublePositives([1, -2, 3, 0, 4.5])).toEqual([2, 6, 9]);
  });

  it("ignores invalid entries", () => {
    expect(doublePositives([1, "2", Number.NaN, Number.POSITIVE_INFINITY, null])).toEqual([2]);
  });

  it("rejects non-arrays", () => {
    expect(doublePositives(null)).toBeNull();
  });
});
