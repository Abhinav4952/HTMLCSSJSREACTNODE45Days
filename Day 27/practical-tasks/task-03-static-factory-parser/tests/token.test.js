import { describe, expect, it } from "vitest";
import { Token } from "../src/token.js";

describe("Token.fromString", () => {
  it("parses", () => {
    const t = Token.fromString("  name : Ada ");
    expect(t).toBeInstanceOf(Token);
    expect(t.kind).toBe("name");
    expect(t.value).toBe("Ada");
  });

  it("rejects bad input", () => {
    expect(Token.fromString("nocolon")).toBeNull();
  });
});
