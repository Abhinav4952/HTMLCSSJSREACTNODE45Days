import { describe, expect, it } from "vitest";
import { Dog } from "../src/dog.js";

describe("Dog", () => {
  it("uses super", () => {
    const d = new Dog("Rex", "corgi");
    expect(d.speak()).toBe("Rex says something (corgi)");
  });
});
