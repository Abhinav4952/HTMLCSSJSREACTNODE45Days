import { describe, expect, it } from "vitest";
import { Box, isBox } from "../src/boxes.js";

describe("Box + instanceof", () => {
  it("works with new", () => {
    expect(isBox(new Box(1))).toBe(true);
  });

  it("callable without new", () => {
    expect(isBox(Box(2))).toBe(true);
  });
});
