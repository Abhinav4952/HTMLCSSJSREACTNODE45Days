import { describe, expect, it } from "vitest";
import { readInherited } from "../src/chainLookup.js";

describe("readInherited", () => {
  it("finds own before inherited", () => {
    const base = { a: 1 };
    const child = Object.assign(Object.create(base), { b: 2 });
    expect(readInherited(child, "b")).toBe(2);
    expect(readInherited(child, "a")).toBe(1);
  });
});
