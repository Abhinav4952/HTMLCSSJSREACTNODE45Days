import { describe, expect, it } from "vitest";
import { prepend, shallowMerge } from "../src/spreadLab.js";

describe("shallowMerge", () => {
  it("merges plain objects with patch precedence", () => {
    expect(shallowMerge({ a: 1, b: 2 }, { b: 9, c: 3 })).toEqual({ a: 1, b: 9, c: 3 });
  });

  it("rejects non-plain objects", () => {
    expect(shallowMerge([], {})).toBeNull();
    expect(shallowMerge({}, new Map())).toBeNull();
  });
});

describe("prepend", () => {
  it("prepends to arrays immutably-ish (returns new array)", () => {
    const base = [2, 3];
    const next = prepend(base, 1);
    expect(next).toEqual([1, 2, 3]);
    expect(base).toEqual([2, 3]);
  });

  it("rejects non-arrays", () => {
    expect(prepend(null, 1)).toBeNull();
  });
});
