import { describe, expect, it } from "vitest";
import { parseKeyValueLines } from "../src/yamlKeys.js";

describe("parseKeyValueLines", () => {
  it("parses lines", () => {
    expect(parseKeyValueLines("a: 1\nb: two")).toEqual({ a: "1", b: "two" });
  });
});
