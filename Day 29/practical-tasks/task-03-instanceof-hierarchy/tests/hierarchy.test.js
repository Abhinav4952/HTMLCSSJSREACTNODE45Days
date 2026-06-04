import { describe, expect, it } from "vitest";
import { Animal, Dog, classifyPet } from "../src/hierarchy.js";

describe("classifyPet", () => {
  it("uses instanceof", () => {
    expect(classifyPet(new Dog("a", "b"))).toBe("dog");
    expect(classifyPet(new Animal("a"))).toBe("animal");
    expect(classifyPet({})).toBe("unknown");
  });
});
