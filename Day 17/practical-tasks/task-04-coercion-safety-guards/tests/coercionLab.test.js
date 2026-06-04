import { describe, expect, it } from "vitest";
import { stringifyForLog, toIntegerOrNull } from "../src/coercionLab.js";

describe("toIntegerOrNull", () => {
  it("handles nullish", () => {
    expect(toIntegerOrNull(null)).toBeNull();
    expect(toIntegerOrNull(undefined)).toBeNull();
  });

  it("maps booleans to 0/1", () => {
    expect(toIntegerOrNull(true)).toBe(1);
    expect(toIntegerOrNull(false)).toBe(0);
  });

  it("truncates finite numbers toward zero", () => {
    expect(toIntegerOrNull(12.9)).toBe(12);
    expect(toIntegerOrNull(-3.9)).toBe(-3);
  });

  it("parses integer strings", () => {
    expect(toIntegerOrNull("  007 ")).toBe(7);
    expect(toIntegerOrNull("-12")).toBe(-12);
  });

  it("returns null for invalid numbers/strings/types", () => {
    expect(toIntegerOrNull(Number.NaN)).toBeNull();
    expect(toIntegerOrNull(Number.POSITIVE_INFINITY)).toBeNull();
    expect(toIntegerOrNull("12.3")).toBeNull();
    expect(toIntegerOrNull("12px")).toBeNull();
    expect(toIntegerOrNull("")).toBeNull();
    expect(toIntegerOrNull("   ")).toBeNull();
    expect(toIntegerOrNull({})).toBeNull();
    expect(toIntegerOrNull(() => 1)).toBeNull();
  });
});

describe("stringifyForLog", () => {
  it("uses JSON.stringify for arrays/objects", () => {
    expect(stringifyForLog({ a: 1 })).toBe('{"a":1}');
    expect(stringifyForLog([1, 2])).toBe("[1,2]");
  });

  it("uses String for primitives", () => {
    expect(stringifyForLog(null)).toBe("null");
    expect(stringifyForLog(undefined)).toBe("undefined");
    expect(stringifyForLog(12)).toBe("12");
  });
});
