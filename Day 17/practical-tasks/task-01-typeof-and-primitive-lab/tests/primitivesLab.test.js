import { describe, expect, it } from "vitest";
import { isPrimitiveValue, typeLabel } from "../src/primitivesLab.js";

describe("isPrimitiveValue", () => {
  it("treats null and undefined as primitives", () => {
    expect(isPrimitiveValue(null)).toBe(true);
    expect(isPrimitiveValue(undefined)).toBe(true);
  });

  it("treats common primitives as primitives", () => {
    expect(isPrimitiveValue("hi")).toBe(true);
    expect(isPrimitiveValue(0)).toBe(true);
    expect(isPrimitiveValue(false)).toBe(true);
    expect(isPrimitiveValue(123n)).toBe(true);
    expect(isPrimitiveValue(Symbol("x"))).toBe(true);
  });

  it("treats objects/functions/arrays as non-primitives", () => {
    expect(isPrimitiveValue({})).toBe(false);
    expect(isPrimitiveValue([])).toBe(false);
    expect(isPrimitiveValue(() => {})).toBe(false);
  });
});

describe("typeLabel", () => {
  it("labels null distinctly", () => {
    expect(typeLabel(null)).toBe("null");
  });

  it("uses typeof for primitives (non-null)", () => {
    expect(typeLabel(undefined)).toBe("undefined");
    expect(typeLabel("x")).toBe("string");
    expect(typeLabel(1)).toBe("number");
    expect(typeLabel(true)).toBe("boolean");
    expect(typeLabel(1n)).toBe("bigint");
    expect(typeLabel(Symbol("a"))).toBe("symbol");
  });

  it("labels arrays, functions, and plain objects", () => {
    expect(typeLabel([])).toBe("array");
    expect(typeLabel([1, 2])).toBe("array");
    expect(typeLabel(() => 1)).toBe("function");
    expect(typeLabel(function () {})).toBe("function");
    expect(typeLabel({ a: 1 })).toBe("object");
  });
});

