import { describe, expect, it } from "vitest";
import { defaultPort, defaultTitle } from "../src/nullishLab.js";

describe("defaultPort", () => {
  it("defaults nullish only", () => {
    expect(defaultPort(null)).toBe(3000);
    expect(defaultPort(undefined)).toBe(3000);
    expect(defaultPort(0)).toBe(0);
  });
});

describe("defaultTitle", () => {
  it("preserves empty string", () => {
    expect(defaultTitle("")).toBe("");
  });

  it("defaults undefined/null", () => {
    expect(defaultTitle(undefined)).toBe("Untitled");
    expect(defaultTitle(null)).toBe("Untitled");
  });
});
