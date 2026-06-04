import { describe, expect, it } from "vitest";
import {
  blockShadowValue,
  constObjectPropertyMutation,
  letLoopClosureMappedValues,
  varLoopClosureMappedValues,
} from "../src/scopeLab.js";

describe("varLoopClosureMappedValues", () => {
  it("captures one shared binding (classic trap)", () => {
    expect(varLoopClosureMappedValues()).toEqual([3, 3, 3]);
  });
});

describe("letLoopClosureMappedValues", () => {
  it("captures per-iteration values", () => {
    expect(letLoopClosureMappedValues()).toEqual([0, 1, 2]);
  });
});

describe("blockShadowValue", () => {
  it("returns inner block shadowed value", () => {
    expect(blockShadowValue()).toBe(2);
  });
});

describe("constObjectPropertyMutation", () => {
  it("allows mutating properties on a const object", () => {
    expect(constObjectPropertyMutation()).toBe(7);
  });
});
