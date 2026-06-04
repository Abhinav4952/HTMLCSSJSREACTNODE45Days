import { describe, expect, it } from "vitest";
import { createObjectMetadata } from "../src/metaWeak.js";

describe("WeakMap metadata", () => {
  it("tags objects", () => {
    const m = createObjectMetadata();
    const o = {};
    m.tag(o, "first");
    expect(m.read(o)).toBe("first");
  });
});
