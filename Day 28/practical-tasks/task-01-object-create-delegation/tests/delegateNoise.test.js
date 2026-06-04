import { describe, expect, it } from "vitest";
import { createNoisyThing } from "../src/delegateNoise.js";

describe("createNoisyThing", () => {
  it("delegates label()", () => {
    const dog = createNoisyThing("dog");
    expect(dog.label()).toBe("dog");
  });
});
