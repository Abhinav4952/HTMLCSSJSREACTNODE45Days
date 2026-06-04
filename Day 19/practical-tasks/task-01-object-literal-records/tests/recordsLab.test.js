import { describe, expect, it } from "vitest";
import { shallowMergeRecords } from "../src/recordsLab.js";

describe("shallowMergeRecords", () => {
  it("merges shallowly with later keys winning", () => {
    expect(shallowMergeRecords({ a: 1, b: 2 }, { b: 9, c: 3 })).toEqual({ a: 1, b: 9, c: 3 });
  });

  it("rejects non-plain objects", () => {
    expect(shallowMergeRecords(null, {})).toBeNull();
    expect(shallowMergeRecords({}, null)).toBeNull();
    expect(shallowMergeRecords([], {})).toBeNull();
    expect(shallowMergeRecords({}, new Map())).toBeNull();
  });

  it("supports null-prototype objects", () => {
    const a = Object.create(null);
    a.x = 1;
    const b = { y: 2 };
    expect(shallowMergeRecords(a, b)).toEqual({ x: 1, y: 2 });
  });
});
