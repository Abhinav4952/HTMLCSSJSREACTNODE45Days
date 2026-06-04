import { describe, expect, it } from "vitest";
import { objectFromEntries, pickOwn } from "../src/keysLab.js";

describe("pickOwn", () => {
  it("picks own keys in order", () => {
    const src = { a: 1, b: 2, c: 3 };
    expect(pickOwn(src, ["c", "a", "missing"])).toEqual({ c: 3, a: 1 });
  });

  it("rejects non-plain objects and non-array keys", () => {
    expect(pickOwn(null, [])).toBeNull();
    expect(pickOwn({}, null)).toBeNull();
    expect(pickOwn([], ["x"])).toBeNull();
  });
});

describe("objectFromEntries", () => {
  it("builds objects from k/v pairs", () => {
    expect(
      objectFromEntries([
        ["a", 1],
        ["b", 2],
      ]),
    ).toEqual({ a: 1, b: 2 });
  });

  it("lets later duplicates win", () => {
    expect(
      objectFromEntries([
        ["x", 1],
        ["x", 9],
      ]),
    ).toEqual({ x: 9 });
  });

  it("ignores invalid rows", () => {
    expect(objectFromEntries([["ok", 1], null, ["", 2], ["bad", 3], 123])).toEqual({ ok: 1, bad: 3 });
  });
});
