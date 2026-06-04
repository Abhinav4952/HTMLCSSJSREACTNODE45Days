import { describe, expect, it } from "vitest";
import { buildLabel, repeatText } from "../src/defaultParamsLab.js";

describe("buildLabel", () => {
  it("joins trimmed non-empty parts", () => {
    expect(buildLabel(["  a ", "b", "  "])).toBe("a | b");
  });

  it("uses empty fallback when everything trims away", () => {
    expect(buildLabel(["", "   "])).toBe("(none)");
  });

  it("honors custom separator and fallback", () => {
    expect(buildLabel(["x", "y"], ",", "empty")).toBe("x,y");
    expect(buildLabel(["  ", " "], ",", "empty")).toBe("empty");
  });

  it("rejects non-array parts", () => {
    expect(buildLabel(undefined)).toBeNull();
  });
});

describe("repeatText", () => {
  it("repeats with default times", () => {
    expect(repeatText("ha")).toBe("ha");
  });

  it("returns empty for non-string text", () => {
    expect(repeatText(null, 3)).toBe("");
  });

  it("clamps invalid times toward safe small repeats", () => {
    expect(repeatText("*", 0)).toBe("");
    expect(repeatText("*", 3)).toBe("***");
    expect(repeatText("*", 999)).toBe("*"); // invalid -> treat as 1 per spec
  });
});
