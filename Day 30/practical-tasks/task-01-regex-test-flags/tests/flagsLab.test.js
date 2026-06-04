import { describe, expect, it } from "vitest";
import { hasCaseInsensitiveYes } from "../src/flagsLab.js";

describe("hasCaseInsensitiveYes", () => {
  it("uses case-insensitive flag", () => {
    expect(hasCaseInsensitiveYes("YES!")).toBe(true);
    expect(hasCaseInsensitiveYes("no")).toBe(false);
  });
});
