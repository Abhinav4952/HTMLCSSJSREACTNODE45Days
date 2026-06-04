import { describe, expect, it } from "vitest";
import { parseJsonSafe } from "../src/safeJson.js";

describe("parseJsonSafe", () => {
  it("parses valid json", () => {
    expect(parseJsonSafe('{"a":1}')).toEqual({ a: 1 });
  });

  it("returns fallback on invalid", () => {
    expect(parseJsonSafe("{", 1)).toBe(1);
  });
});
