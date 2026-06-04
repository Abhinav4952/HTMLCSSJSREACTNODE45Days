import { describe, expect, it } from "vitest";
import { standaloneThisType } from "../src/strictThis.js";

describe("standaloneThisType", () => {
  it("is undefined in strict IIFE", () => {
    expect(standaloneThisType()).toBe("undefined");
  });
});
