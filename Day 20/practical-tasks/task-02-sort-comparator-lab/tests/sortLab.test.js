import { describe, expect, it } from "vitest";
import { sortCaseInsensitive } from "../src/sortLab.js";

describe("sortCaseInsensitive", () => {
  it("sorts ignoring case", () => {
    expect(sortCaseInsensitive(["b", "A", "c"])).toEqual(["A", "b", "c"]);
  });

  it("does not mutate input", () => {
    const input = ["b", "a"];
    const copy = [...input];
    const out = sortCaseInsensitive(input);
    expect(input).toEqual(copy);
    expect(out).not.toBe(input);
  });

  it("ignores non-strings", () => {
    expect(sortCaseInsensitive(["z", 1, "a", null, "m"])).toEqual(["a", "m", "z"]);
  });

  it("rejects non-arrays", () => {
    expect(sortCaseInsensitive(null)).toBeNull();
  });
});
