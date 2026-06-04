import { describe, expect, it } from "vitest";
import { cube, square } from "../src/functionFormsLab.js";

describe("square (declaration)", () => {
  it("squares finite numbers", () => {
    expect(square(3)).toBe(9);
    expect(square(0)).toBe(0);
    expect(square(-4)).toBe(16);
  });

  it("returns NaN for invalid inputs", () => {
    expect(Number.isNaN(square("3"))).toBe(true);
    expect(Number.isNaN(square(Number.NaN))).toBe(true);
    expect(Number.isNaN(square(Number.POSITIVE_INFINITY))).toBe(true);
  });
});

describe("cube (function expression)", () => {
  it("cubes finite numbers", () => {
    expect(cube(2)).toBe(8);
    expect(cube(-1)).toBe(-1);
  });

  it("returns NaN for invalid inputs", () => {
    expect(Number.isNaN(cube(null))).toBe(true);
  });

  it("is a function value on a const binding", () => {
    expect(typeof cube).toBe("function");
  });
});
