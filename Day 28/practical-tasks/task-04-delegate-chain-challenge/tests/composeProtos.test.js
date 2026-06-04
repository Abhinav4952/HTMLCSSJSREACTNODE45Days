import { describe, expect, it } from "vitest";
import { composeDefaults } from "../src/composeProtos.js";

describe("composeDefaults", () => {
  it("inherits missing keys from base", () => {
    const base = { a: 1, b: 2 };
    const obj = composeDefaults(base, { b: 9, c: 3 });
    expect(obj.b).toBe(9);
    expect(obj.a).toBe(1);
    expect(Object.prototype.hasOwnProperty.call(obj, "a")).toBe(false);
  });
});
