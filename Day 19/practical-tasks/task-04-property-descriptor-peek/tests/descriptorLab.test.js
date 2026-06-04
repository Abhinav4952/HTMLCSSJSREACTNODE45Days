import { describe, expect, it } from "vitest";
import { summarizeOwnDataDescriptor } from "../src/descriptorLab.js";

describe("summarizeOwnDataDescriptor", () => {
  it("summarizes a normal data property", () => {
    const obj = { a: 1 };
    expect(summarizeOwnDataDescriptor(obj, "a")).toEqual({
      writable: true,
      enumerable: true,
      configurable: true,
    });
  });

  it("returns null for missing or inherited keys", () => {
    const proto = { a: 1 };
    const obj = Object.create(proto);
    expect(summarizeOwnDataDescriptor(obj, "a")).toBeNull();
    expect(summarizeOwnDataDescriptor(obj, "missing")).toBeNull();
  });

  it("returns null for accessor descriptors", () => {
    const obj = {};
    Object.defineProperty(obj, "x", {
      enumerable: true,
      configurable: true,
      get() {
        return 1;
      },
    });
    expect(summarizeOwnDataDescriptor(obj, "x")).toBeNull();
  });

  it("rejects non-objects", () => {
    expect(summarizeOwnDataDescriptor(null, "a")).toBeNull();
    expect(summarizeOwnDataDescriptor("hi", "0")).toBeNull();
  });
});
