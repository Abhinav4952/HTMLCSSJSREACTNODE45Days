import { describe, expect, it } from "vitest";
import { Animal } from "../src/animal.js";

describe("Animal", () => {
  it("speaks with name", () => {
    expect(new Animal("Ada").speak()).toBe("Ada says something");
  });

  it("handles missing name", () => {
    expect(new Animal().speak()).toBe("...");
  });
});
