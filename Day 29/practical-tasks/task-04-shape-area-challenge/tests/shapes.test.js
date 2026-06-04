import { describe, expect, it } from "vitest";
import { Rectangle, Square } from "../src/shapes.js";

describe("Shapes", () => {
  it("computes rectangle area", () => {
    expect(new Rectangle(3, 4).area()).toBe(12);
  });

  it("square uses super", () => {
    expect(new Square(5).area()).toBe(25);
  });
});
